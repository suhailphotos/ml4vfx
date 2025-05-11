from __future__ import annotations

import os
from pathlib import Path

from bookslib.book import Book
from bookslib.library import Library


# ---------------------------------------------------------------------
# Helper: choose a database path
# ---------------------------------------------------------------------
def resolve_db_path() -> Path:
    """
    • If we're inside the editable checkout (project root has pyproject.toml)
      puts books_db.json next to that file.
    • Otherwise (installed package) → use ~/.books_lib_db.json
    """
    pkg_dir = Path(__file__).resolve().parent   
    project_root = pkg_dir.parent.parent    
    if (project_root / "pyproject.toml").exists():
        return project_root / "books_db.json"

    # Fallback for end-users
    return Path.home() / ".books_lib_db.json"


DB_PATH: Path = resolve_db_path()
DB_PATH.touch(exist_ok=True)


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------
def main() -> None:
    lib = Library(str(DB_PATH))

    # 1) Search -------------------------------------------------------
    print("Searching for 'mockingbird'…")
    lib.search_books("mockingbird")
    print("-" * 24)

    # 2) Total count --------------------------------------------------
    print("Total books in the current library:")
    print(f"Total books count: {lib.get_total_book_count()}")
    print("-" * 24)

    # 3) Add two books ------------------------------------------------
    print("Adding books to the library…")
    book1 = Book(
        title="The Great Gatsby",
        authors=["F. Scott Fitzgerald"],
        publisher="Charles Scribner's Sons",
        isbn="9780743273565",
        publication_year=1925,
        num_pages=218,
    )
    book2 = Book(
        title="Dune",
        authors=["Frank Herbert"],
        publisher="Chilton Books",
        isbn="9780441013593",
        publication_year=1965,
        num_pages=412,
    )
    lib.add_book_to_library(book1)
    lib.add_book_to_library(book2)
    print("-" * 24)

    # 4) List everything ---------------------------------------------
    print("Getting all the books in the library:")
    lib.get_all_books(verbose=1)
    print("-" * 24)

    # 5) Remove by query ---------------------------------------------
    print("Removing all books matching 'gatsby':")
    lib.remove_books_from_library_by_query("gatsby")
    print("-" * 24)

    # 6) Remove one by selection -------------------------------------
    print("Removing a specific book by selection:")
    lib.remove_books_from_library_by_selection()
    print("-" * 24)

    # 7) Final state --------------------------------------------------
    print("All current books in the library:")
    lib.get_all_books(verbose=1)
    print("-" * 24)


if __name__ == "__main__":
    """
    booksLib package
    • Auto-creates a JSON DB on first run.
    • Works both from a source checkout AND an installed package.
    Run with:
        python -m bookslib
        -----   or ------
        poetry run bookslib-demo
    """
    main()
