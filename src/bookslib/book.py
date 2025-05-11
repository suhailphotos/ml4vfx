# src/book.py

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional

from bookslib.utils import LibraryUtils
# ---------------------------------------------------------------------
# `order=True` lets us sort by field order (title → authors → …).
# `compare=False` on *id* keeps UUID out of equality ordering, but the
# field is still present and hashable.
# ---------------------------------------------------------------------
@dataclass(frozen=True, order=True, slots=True)
class Book:
    title: str
    authors: List[str]
    publisher: str
    isbn: str
    publication_year: int
    language: str = "English"
    num_pages: Optional[int] = None
    id: str = field(
        default_factory=LibraryUtils.generate_book_uuid,
        compare=False,
    )

    # -----------------------------------------------------------------
    @property
    def authors_string(self) -> str:
        """Return authors joined into one readable string."""
        return ", ".join(self.authors)

    @property
    def search_string(self) -> str:
        """
        Case-folded concatenation of common fields — handy for
        substring searches inside `Library.search()`.
        """
        return (
            f"{self.title} "
            f"{self.authors_string} "
            f"{self.publisher} "
            f"{self.isbn} "
            f"{self.publication_year}"
        ).lower()

    # -----------------------------------------------------------------
    def to_dict(self) -> dict:
        """
        Serialize to a plain dict ready for JSONBackend.
        """
        return asdict(self)

if __name__ == "__main__":
    import json

    # 1) CREATE
    book = Book(
        title="The Hobbit",
        authors=["J.R.R. Tolkien"],
        publisher="George Allen & Unwin",
        isbn="978-0547928227",
        publication_year=1937,
        language="English",
        num_pages=310
    )
    print(f"Created Book: {book}")

    # 2) PROPERTIES
    print("→ id:", book.id)
    print("→ authors_string:", book.authors_string)
    print("→ search_string:", book.search_string)

    # 3) SERIALIZATION
    book_dict = book.to_dict()
    print("→ as dict:")
    print(json.dumps(book_dict, indent=4))

    # 4) BASIC SMOKE CHECK
    if (
        isinstance(book.id, str)
        and "The Hobbit" in book_dict["title"]
        and "J.R.R. Tolkien" in book_dict["authors"]
    ):
        print("Book class is working correctly!")
    else:
        print("Something’s wrong with Book implementation.")
