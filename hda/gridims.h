// function to compute grid dimentions
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
