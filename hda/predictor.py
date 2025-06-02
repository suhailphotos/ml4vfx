"""
An attribute Wrangle upstream in the hda computes the grid dimentions
VEX code:
void getGridSize(int geo; export int rows; export int cols)
{
    int PR = nprimitives(geo);
    if (PR < 2) { rows = cols = 0; return; }

    vector c0 = primuv(geo, "P", 0, {0.5,0.5,0});
    vector c1 = primuv(geo, "P", 1, {0.5,0.5,0});
    vector d  = c1 - c0;

    int rowAxis = (abs(d.x)>=abs(d.y) && abs(d.x)>=abs(d.z)) ? 0
                : (abs(d.y)>=abs(d.z))                          ? 1
                : 2;
    int cA = (rowAxis==0?1:0), cB = (rowAxis==2?1:2);
    float eps = 1e-6; int PC=0;

    for (int p=0; p<PR; p++) {
        vector cp = primuv(geo,"P",p,{0.5,0.5,0});
        if (abs(cp[cA]-c0[cA])<eps && abs(cp[cB]-c0[cB])<eps)
            PC++;
        else
            break;
    }

    int PROWS = PR/PC;
    rows = PROWS;
    cols = PC;
}

int ptR, ptC; getGridSize(0, ptR, ptC);
setdetailattrib(0, "grid_rows", ptR, "set");
setdetailattrib(0, "grid_cols", ptC, "set");

"""
import numpy as np
from PIL import Image
import requests
import hou
import os
import io

def predict_from_grid(node):
    geo = node.geometry()
    rows = geo.intAttribValue("grid_rows")
    cols = geo.intAttribValue("grid_cols")

    if rows != cols:
        hou.ui.displayMessage(
            f"Warning: Grid is not square ({rows}x{cols}); image may be distorted.",
            severity=hou.severityType.Warning
        )

    prims = geo.prims()
    cd_array = np.array([prim.attribValue("Cd") for prim in prims])
    gray = np.mean(cd_array, axis=1)
    img_array = (gray.reshape((rows, cols)) * 255).astype(np.uint8)

    img = Image.fromarray(img_array, mode="L")
    if (rows, cols) != (28, 28):
        img = img.resize((28, 28), Image.BILINEAR)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    api_url = os.environ.get("FASHION_API_URL", "http://localhost:8000") + "/predict"
    files = {"file": ("grid.png", buf, "image/png")}
    try:
        resp = requests.post(api_url, files=files, timeout=5)
        resp.raise_for_status()
        result = resp.json()
        label = result.get("label", "Unknown")
        class_id = result.get("class_id", -1)
    except Exception as e:
        label = f"ERROR: {e}"
        class_id = -1

    geo.addAttrib(hou.attribType.Global, "prediction", label)
    geo.addAttrib(hou.attribType.Global, "class_id", class_id)
    print(f"Prediction: {label} (class_id={class_id})")
