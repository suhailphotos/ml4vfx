// ——————————————————————————————————————————————
// Maze-color carve on any axis-aligned quad grid
// Detail Wrangle (Run Over: Detail, Execute Once)
// ——————————————————————————————————————————————

//
// Helper: infer un-parameterized grid size (cell count) from prim centroids
//
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
    rows = PROWS+1;
    cols = PC+1;
}

// 0) get cell dims
int ptR, ptC; getGridSize(0, ptR, ptC);
int cellRows = ptR - 1;
int cellCols = ptC - 1;
if (cellRows<1 || cellCols<1) return;

// 1) init walls
int vcount = cellRows*(cellCols+1);
int hcount = (cellRows+1)*cellCols;
int vwalls[]; resize(vwalls, vcount);
int hwalls[]; resize(hwalls, hcount);
for (int i=0; i<vcount;  i++) vwalls[i]=1;
for (int i=0; i<hcount;  i++) hwalls[i]=1;

// 2) carve with recursive-backtracker
float seed    = chf("seed");
int   loopPct = chi("loop_pct");
int totalCells= cellRows*cellCols;
int visited[]; resize(visited, totalCells);
int stack[]; int start=int(rand(seed)*totalCells);
visited[start]=1; push(stack,start);

while(len(stack)){
    int curr=stack[-1];
    int r=curr/cellCols, c=curr%cellCols;
    int avail[];
    if(c>0        && !visited[curr-1])    push(avail,curr-1);
    if(c<cellCols-1&& !visited[curr+1])   push(avail,curr+1);
    if(r>0        && !visited[curr-cellCols]) push(avail,curr-cellCols);
    if(r<cellRows-1&& !visited[curr+cellCols]) push(avail,curr+cellCols);

    if(len(avail)){
        int pick=avail[int(rand(seed+curr)*len(avail))];
        int pr=pick/cellCols, pc=pick%cellCols;
        if(pr==r){
            int wi=r*(cellCols+1)+max(c,pc);
            vwalls[wi]=0;
        } else {
            int wi=min(r,pr)*cellCols+c;
            hwalls[wi]=0;
        }
        visited[pick]=1;
        push(stack,pick);
    } else {
        pop(stack);
    }
}

// extra loops
int extras=int(loopPct/100.0*(vcount+hcount));
for(int i=0; i<extras; i++){
    if(rand(seed+i)<0.5){
        int wi=int(rand(seed+i*7)*vcount);
        vwalls[wi]=0;
    } else {
        int wi=int(rand(seed+i*13)*hcount);
        hwalls[wi]=0;
    }
}


// 4) paint cells: black if they border any wall, white otherwise
vector colW={0.2,0.2,0.2}, colP={1,1,1};
// 4a: clear to white
for(int p=0;p<totalCells;p++) setprimattrib(0,"Cd",p,colP,"set");
// 4b: vertical walls → adjacent cells black
for(int wi=0;wi<vcount;wi++){
    if(!vwalls[wi]) continue;
    int r=wi/(cellCols+1), c=wi%(cellCols+1);
    if(c>0)    setprimattrib(0,"Cd", r*cellCols+(c-1),colW,"set");
    if(c<cellCols) setprimattrib(0,"Cd", r*cellCols+c, colW,"set");
}
// 4c: horizontal walls → adjacent cells black
for(int wi=0;wi<hcount;wi++){
    if(!hwalls[wi]) continue;
    int r=wi/cellCols, c=wi%cellCols;
    if(r>0)        setprimattrib(0,"Cd",(r-1)*cellCols+c,colW,"set");
    if(r<cellRows) setprimattrib(0,"Cd", r*cellCols+c, colW,"set");
}
