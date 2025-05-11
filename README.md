# Machine‑Learning for VFX & 3D
### ml4vfx

*Course repo for Rebelway’s “Machine Learning for VFX & 3D”*

---

## What is this repo?

This repository is **my personal fork** of the instructor‑maintained code base<br>`pixelknit/rebelwayAppliedML` *(see the original upstream repo ⚑).*

* **Origin** → [https://github.com/suhailphotos/ml4vfx](https://github.com/suhailphotos/ml4vfx) *(this repo)*
* **Upstream** → [https://github.com/pixelknit/rebelwayAppliedML](https://github.com/pixelknit/rebelwayAppliedML)

Forking lets me:

1. **Pull** all new material the instructor pushes.
2. **Commit my own assignments / experiments** without touching upstream.
3. Open PRs to contribute fixes when appropriate.

> **Nothing I commit here is automatically sent upstream**—I keep full control.

---

## Repo layout

```text
ml4vfx/                  ← main branch worktree (this folder)
ml4vfxTrees/             ← container for topic branches
   ├── api/              ← FastAPI + backend utilities
   ├── compBasics/       ← Python, Git, JAX, SOLID refresher
   ├── data3D/           ← 3D data libraries & mesh processing
   ├── dataIO/           ← Houdini HDA for data I/O, MNIST pipeline
   ├── experiments/      ← Sandbox notebooks & Gen‑AI prototypes
   ├── houdini/          ← Houdini‑specific ML nodes & HDAs
   ├── nlp/              ← Text processing, fine‑tuning examples
   ├── reinforce/        ← RL Gym setups & game‑AI demos
   ├── sklearn/          ← Classic ML algorithms & pedagogy
   ├── tensorFlow/       ← TF/Keras pipelines & node prediction
   └── vision/           ← Computer‑vision (pose, depth, mediapipe…)
```

### Why *worktrees*?

Each folder above is a **Git worktree** bound to its own branch. That means I can:

* edit multiple topic branches side‑by‑side, no `git switch` dance
* keep IDE / Jupyter kernels pointed at a single folder
* add or drop topics on demand:

```bash
# add new topic ➜  branch & worktree in one go
cd ml4vfx
git switch -c lighting upstream/lighting
git worktree add ../ml4vfxTrees/lighting lighting

# remove when done
git worktree remove ../ml4vfxTrees/lighting
```

Main (`ml4vfx/`) stays pristine for documentation and course‑wide scripts.

---

## Course breakdown (topic‑centric)

The instructor’s original *week‑by‑week* outline has been regrouped into **topic branches** above. Below is a concise map:

| Topic branch    | Core coverage (excerpt)                                                               |
| --------------- | ------------------------------------------------------------------------------------- |
| **compBasics**  | OS & computer‑arch refresher · Git & Python quickstart · NumPy/JAX · SOLID principles |
| **api**         | FastAPI · blob storage · building REST backends for ML services                       |
| **data3D**      | Point‑cloud extraction · Poisson surface recon · mesh algorithms                      |
| **vision**      | Depth estimation · pose detection (Mediapipe) · AI animation prediction               |
| **houdini**     | Custom HDAs · data I/O nodes · AI QC for assets · node prediction system              |
| **dataIO**      | Dataset ingestion in Houdini · MNIST & PyTorch examples                               |
| **tensorFlow**  | Node‑prediction networks · TF/Keras CNN demos                                         |
| **sklearn**     | Traditional ML algorithms & pedagogy                                                  |
| **nlp**         | Text detectors · LLM fine‑tuning · prompt engineering                                 |
| **reinforce**   | OpenAI Gym · retro game RL · Houdini RL agent experiments                             |
| **experiments** | Gen‑AI texture/geometry generation · synthetic‑data pipelines                         |

*Full course screenshot with the original week‑grid is available in `/assets/course_breakdown.png`.*

---

## Syncing with upstream

```bash
# from *any* worktree folder
git fetch upstream                  # get latest instructor commits

# merge the matching branch
# (ex: vision branch tracks instructor's computer-vision branch)
cd ../ml4vfxTrees/vision
git merge upstream/computer-vision
git push                            # push to my fork
```

Branches not listed above will be added on demand.

---

## Contributing (to my fork)

1. Commit changes in the relevant topic worktree.
2. Push to this repo (`origin`).
3. Optionally open a PR **from** this repo **to** upstream if you think the change benefits the entire class.

---

## License

Content inherited from upstream retains its original license (see each folder).
Additions by me are MIT‑licensed unless noted otherwise.

---

> *“Machines alone do nothing. They only reveal the power of the human imagination.”* – Alan Kay

