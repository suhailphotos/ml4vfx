// Detail Wrangle (Run Over: Detail, Execute Once)

// Fetch grid dims:
int cellRows = detail(0, "rows", 0);
int cellCols = detail(0, "cols", 0);
int total  = cellRows * cellCols;
if (cellRows < 1 || cellCols < 1) return;

// Read open flags into an array:
int openFlags[]; resize(openFlags, total);
for (int p = 0; p < total; p++)
    openFlags[p] = prim(0, "open", p);

// Collect first‐row & last‐row openings:
int firstRowOpens[];   // row 0 → prim indices 0…cellCols-1
int lastRowOpens[];    // row cellRows-1 → prim indices (cellRows-1)*cellCols…end
for (int c = 0; c < cellCols; c++) {
    int idx0 = 0*cellCols + c;
    if (openFlags[idx0]) push(firstRowOpens, idx0);
    int idxL = (cellRows-1)*cellCols + c;
    if (openFlags[idxL]) push(lastRowOpens, idxL);
}

// Ensure point‐Cd exists (won’t touch prim‐Cd)
addpointattrib(0, "Cd", {1,1,1});


// pick one target:
if (len(lastRowOpens) == 0) {
    warning("No openings on last row to place Target!");
} else {
    int pickT = lastRowOpens[int(rand(chf("seed")+1234)*len(lastRowOpens))];
    vector posT = primuv(0, "P", pickT, {0.5,0.5,0});
    int pt = addpoint(0, posT);
    addpointattrib(0, "name", "");                    // ensure name exists
    setpointattrib(0, "name", pt, "Target", "set");

    // color the Target point light grey
    setpointattrib(0, "Cd", pt, {0.4, 0.6, 0.4}, "set");
}

//  pick up to num_npcs distinct NPC starts:
int num_npcs = chi("num_npcs");
int maxNPCs = len(firstRowOpens);
if (num_npcs > maxNPCs) num_npcs = maxNPCs;

int chosen[];           // to avoid duplicates
for (int i = 0; i < num_npcs; i++) {
    float r = rand(chf("seed") + 5678 + i);
    int pickI = firstRowOpens[int(r * len(firstRowOpens))];
    // avoid duplicates
    if (find(chosen, pickI) >= 0) {
        // if already chosen, skip and try next i
        continue;
    }
    push(chosen, pickI);

    vector posN = primuv(0, "P", pickI, {0.5,0.5,0});
    int ptN = addpoint(0, posN);

    string nm = sprintf("NPC%d", i+1);
    addpointattrib(0, "name", "");               // ensure name exists
    setpointattrib(0, "name", ptN, nm, "set");

    // give each NPC its own random color
    float cr = rand(chf("seed") + i*11);
    float cg = rand(chf("seed") + i*17);
    float cb = rand(chf("seed") + i*23);
    setpointattrib(0, "Cd", ptN, set(cr, cg, cb), "set");
}
