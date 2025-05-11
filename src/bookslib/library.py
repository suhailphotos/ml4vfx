# src/library.py

from __future__ import annotations

import json  # only used for pretty-print fallback
from dataclasses import dataclass, field
from typing import Dict, List

from bookslib.book import Book
from bookslib.db import JSONBackend, StorageBackend
from bookslib.utils import LibraryUtils


# ---------------------------------------------------------------------
@dataclass
class Library:
    """
    database_path : str
        File path for the JSON “database”.
    """

    database_path: str
    is_empty: bool = True
    id: str = field(init=False, default_factory=LibraryUtils.generate_book_uuid)

    # -----------------------------------------------------------------
    def __post_init__(self) -> None:
        # create concrete backend on the fly
        self._backend: StorageBackend = JSONBackend(self.database_path)
        self._refresh_flags()

    # -----------------------------------------------------------------
    # Internal helper to keep is_empty up to date
    def _refresh_flags(self) -> None:
        self.is_empty = len(self._backend.fetch_existing_entries()) == 0

    # -----------------------------------------------------------------
    # CRUD public API
    # -----------------------------------------------------------------
    def get_all_books(self, verbose: int = 0) -> Dict[str, dict]:
        """
        Return every book record (keyed by UUID).

        verbose=1 → print friendly listing (similar to Fstream.print_json_structure).
        """
        entries = self._backend.fetch_existing_entries()
        self._refresh_flags()

        if verbose == 1:
            if entries:
                JSONBackend.print_entries(entries)
            else:
                print("<< library is empty >>")
        elif verbose not in (0, 1):
            raise ValueError("verbose must be 0 or 1")

        return entries

    # -----------------------------------------------------------------
    def search_books(self, query: str) -> List[Book]:
        entries = self.get_all_books()
        hits: List[Book] = []

        for b_dict in entries.values():
            book = Book(**b_dict)
            if query.lower() in book.search_string:
                hits.append(book)

        if hits:
            for b in hits:
                print(f"Found: {b.title}  —  {b.authors_string}")
        else:
            print("No books found")

        return hits

    # -----------------------------------------------------------------
    def get_total_book_count(self) -> int:
        """Return total # of books in the library."""
        return len(self.get_all_books())

    # -----------------------------------------------------------------
    def add_book_to_library(self, book: Book) -> None:
        """Add a new `Book` and persist immediately."""
        self._backend.create_entry(book.to_dict())
        self._refresh_flags()
        print(f"Added '{book.title}' to the library.")

    # -----------------------------------------------------------------
    def remove_books_from_library_by_query(self, query: str) -> None:
        """
        Bulk-delete any book where *query* is a case-insensitive substring
        of its `search_string`.
        """
        entries = self.get_all_books()
        to_remove = [
            bid
            for bid, b_dict in entries.items()
            if query.lower() in Book(**b_dict).search_string
        ]

        if not to_remove:
            print(f"No books found matching '{query}'")
            return

        for bid in to_remove:
            title = entries[bid]["title"]
            self._backend.delete_entry(bid)
            print(f"Removed '{title}'")

        self._refresh_flags()

    # -----------------------------------------------------------------
    def remove_books_from_library_by_selection(self) -> None:
        """Interactive picker that lists books and lets the user delete one."""
        entries = self.get_all_books()
        ids = list(entries.keys())

        if not ids:
            print("Library is empty.")
            return

        for idx, bid in enumerate(ids, start=1):
            b = entries[bid]
            print(f"{idx}: {b['title']}  —  {', '.join(b['authors'])}")

        try:
            choice = int(input("Select a book to delete (number): ")) - 1
        except ValueError as exc:
            raise ValueError("You must enter a number!") from exc

        if choice < 0 or choice >= len(ids):
            print("Book not found!")
            return

        bid = ids[choice]
        removed_title = entries[bid]["title"]
        self._backend.delete_entry(bid)
        print(f"Removed '{removed_title}'")
        self._refresh_flags()

    # -----------------------------------------------------------------
    def empty_library(self) -> None:
        """Delete **all** books."""
        entries = self.get_all_books()
        if not entries:
            print("Library is already empty")
            return

        for bid in list(entries.keys()):
            self._backend.delete_entry(bid)

        self._refresh_flags()
        print("The library is now empty.")

if __name__ == "__main__":
    import os

    test_file = "test_library.json"
    # start fresh
    if os.path.exists(test_file):
        os.remove(test_file)

    lib = Library(test_file)

    # 1) initial state
    print("Initial library:")
    lib.get_all_books(verbose=1)

    # 2) add two books
    b1 = Book(
        title="The Hobbit",
        authors=["J.R.R. Tolkien"],
        publisher="George Allen & Unwin",
        isbn="978-0547928227",
        publication_year=1937,
        language="English",
        num_pages=310
    )
    b2 = Book(
        title="1984",
        authors=["George Orwell"],
        publisher="Secker & Warburg",
        isbn="9780451524935",
        publication_year=1949,
        language="English",
        num_pages=328
    )
    lib.add_book_to_library(b1)
    lib.add_book_to_library(b2)
    print("\nAfter adding books:")
    lib.get_all_books(verbose=1)

    # 3) search
    print("\nSearch for 'hobbit':")
    lib.search_books("hobbit")

    # 4) remove by query
    print("\nRemoving '1984' via query:")
    lib.remove_books_from_library_by_query("1984")
    print("\nAfter removal:")
    lib.get_all_books(verbose=1)

    # 5) empty library
    print("\nEmptying library:")
    lib.empty_library()
    print("\nAfter emptying:")
    lib.get_all_books(verbose=1)

    # cleanup
    os.remove(test_file)
    print("\nCleaned up test file")
