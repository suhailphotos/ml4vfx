# booksLib Week 1 Assignment

**Main Repository:** https://github.com/suhailphotos/ml4vfx.git  
**Worktree Branch:** `booksLib`

---

## Project Structure

```
booksLib/
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── src/
│   └── bookslib/
│       ├── book.py
│       ├── db.py
│       ├── __init__.py
│       ├── library.py
│       ├── __main__.py
│       └── utils.py
└── tests/
    └── __init__.py
```

Source code path:  
https://github.com/suhailphotos/ml4vfx/tree/booksLib/src/bookslib

---

## Local Setup & Demo Run

1. **Clone ONLY the `booksLib` branch**  
   ```bash
   git clone \
     --branch booksLib \
     --single-branch \
     https://github.com/suhailphotos/ml4vfx.git \
     booksLib
   cd booksLib
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
   ```

3. **Install the package (editable) and demo script**  
   ```bash
   pip install --upgrade pip
   pip install .
   ```

4. **Run the demo**  
   ```bash
   bookslib-demo       # via console-script
   # or
   python -m bookslib  # entry-point in __main__.py
   ```
