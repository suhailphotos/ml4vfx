# booksLib – Week 1 Assignment

**Main repository:** <https://github.com/suhailphotos/ml4vfx.git>  
**Worktree branch:** `booksLib`

---

## Project layout

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
    ├── test_book.py
    ├── test_library.py
    └── test_database.json
```

*Source code root:*  
<https://github.com/suhailphotos/ml4vfx/tree/booksLib/src/bookslib>

---

## Key differences vs. the original “shopping‑cart” sample

| Aspect | Shopping‑cart demo | **booksLib** |
|--------|-------------------|--------------|
| **Persistence abstraction** | Direct `json` helper (`Fstream`) | `StorageBackend` interface → swap JSON for SQLite/Postgres later |
| **JSON schema** | Top‑level map keyed by random ID | List of book dictionaries (`{"books": [...]}`) |
| **Why list‑of‑dicts?** |  | * Search often happens by ISBN / title before the UUID is known  <br> * Append‑only and human‑readable  <br> * `JSONBackend.fetch_existing_entries()` converts the list to `{id: entry}` in memory, so look‑ups stay O(1). |

### Sample schema

```json
{
  "books": [
    {
      "id": "6f1a4b4e-3c9d-4e2c-bc7b-4b3d9e8f1c2a",
      "title": "To Kill a Mockingbird",
      "authors": ["Harper Lee"],
      "publisher": "J.B. Lippincott & Co.",
      "isbn": "9780061120084",
      "publication_year": 1960,
      "language": "English",
      "num_pages": 281
    },
    {
      "id": "b2d1e8a7-5c4f-4f3d-8e2a-7f9e6c8b5d1a",
      "title": "1984",
      "authors": ["George Orwell"],
      "publisher": "Secker & Warburg",
      "isbn": "9780451524935",
      "publication_year": 1949,
      "language": "English",
      "num_pages": 328
    }
  ]
}
```

---

## Local setup & demo run


### 1) clone only the worktree branch
```bash
git clone   --branch booksLib   --single-branch   https://github.com/suhailphotos/ml4vfx.git   booksLib
cd booksLib
```

### 2) create & activate virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

### 3) install package in editable mode + console script
```bash
pip install --upgrade pip
pip install .
```

### 4) run the demo
```bash
bookslib-demo       # console script
#   or
python -m bookslib  # __main__.py entry‑point
```

The first run creates `books_db.json` (in project root when running from source, or in `~/.books_lib_db.json` when installed globally).
