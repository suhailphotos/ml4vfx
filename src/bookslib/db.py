# src/db.py

from __future__ import annotations

import json
import os
from typing import Dict, List

# --------------------------------------------------------------------
# Pluggable storage interface: enforces class structure for CRUD operations 
# --------------------------------------------------------------------
class StorageBackend:
    """
    Interface for swap-in data backends (JSON, SQLite, etc.).

    Each record is a plain dict produced by `Book.to_dict()`, keyed by
    its unique *id*.
    """
    # ------------------ CRUD Methods ----------------------------------

    # ------------------------- READ -----------------------------------
    def fetch_existing_entries(self) -> Dict[str, dict]:
        """Return current records as {id: entry_dict, ...}."""
        raise NotImplementedError

    # -------------------------- CREATE ---------------------------------
    def create_entry(self, entry: dict) -> None:
        """Insert a new record; must not overwrite an existing id."""
        raise NotImplementedError

    # --------------------------- UPDATE --------------------------------
    def update_entry(self, entry: dict) -> None:
        """Replace the record with the same `id`."""
        raise NotImplementedError

    # --------------------------- DELETE --------------------------------
    def delete_entry(self, entry_id: str) -> None:
        """Remove the record whose key matches *entry_id*."""
        raise NotImplementedError

# --------------------------------------------------------------------
# json as a database
# --------------------------------------------------------------------
class JSONBackend(StorageBackend):
    """
    database format:
    {
        "books": [ {..book1..}, {..book2..}, ... ]
    }
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        # Ensure file exists with an empty skeleton
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"books": []}, f, indent=4)

    # ----------------------- internal helpers ------------------------
    def _read(self) -> List[dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)["books"]

    def _write(self, books: List[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({"books": books}, f, indent=4)

    # ---------------------- interface methods ------------------------
    def fetch_existing_entries(self) -> Dict[str, dict]:
        return {b["id"]: b for b in self._read()}

    def create_entry(self, entry: dict) -> None:
        books = self._read()
        books.append(entry)
        self._write(books)

    def update_entry(self, entry: dict) -> None:
        books = self._read()
        for i, b in enumerate(books):
            if b["id"] == entry["id"]:
                books[i] = entry
                break
        else:  # id not found
            raise KeyError(f"id {entry['id']} not found")
        self._write(books)

    def delete_entry(self, entry_id: str) -> None:
        books = self._read()
        books = [b for b in books if b["id"] != entry_id]
        self._write(books)

    # Optional helper ------------

    @staticmethod
    def print_entries(entries: Dict[str, dict]) -> None:
        """
        Pretty-print the mapping produced by ``fetch_existing_entries``.
        """
        if not entries:
            print("<< no entries >>")
            return
        for k, v in entries.items():
            print(k, "→", v["title"])

if __name__ == "__main__":
    import os
    from bookslib.utils import LibraryUtils

    test_file = "test_books.json"
    # start fresh
    if os.path.exists(test_file):
        os.remove(test_file)

    backend = JSONBackend(test_file)

    # 1) READ: initial state
    print("Initial entries:")
    backend.print_entries(backend.fetch_existing_entries())

    # 2) CREATE
    new_id = LibraryUtils.generate_book_uuid()
    new_book = {
        "id": new_id,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "authors": ["Douglas Adams"],
        "publisher": "Pan Books",
        "isbn": "9780330508537",
        "publication_year": 1979,
        "language": "English",
        "num_pages": 224
    }
    backend.create_entry(new_book)
    print(f'Added "{new_book["title"]}" (id={new_id})')
    backend.print_entries(backend.fetch_existing_entries())

    # 3) UPDATE
    updated = dict(new_book)
    updated["title"] = "The Ultimate Hitchhiker's Guide"
    backend.update_entry(updated)
    print(f'Renamed book id={new_id} to "{updated["title"]}"')
    backend.print_entries(backend.fetch_existing_entries())

    # 4) DELETE
    backend.delete_entry(new_id)
    print(f"Deleted book id={new_id}")
    backend.print_entries(backend.fetch_existing_entries())

    # cleanup
    os.remove(test_file)
    print("Cleaned up test file")
