# tests/test_library.py

from pathlib import Path
import pytest

from bookslib.book import Book
from bookslib.library import Library


@pytest.fixture
def lib(tmp_path: Path):
    src = Path(__file__).with_name("test_database.json")
    db_file = tmp_path / "db.json"
    db_file.write_text(src.read_text())

    lib = Library(str(db_file))
    lib.empty_library() 
    return lib


def test_add_and_count(lib: Library):
    b1 = Book(
        title="Book 1",
        authors=["A"],
        publisher="P",
        isbn="10",
        publication_year=2024,
    )
    b2 = Book(
        title="Book 2",
        authors=["B"],
        publisher="P",
        isbn="11",
        publication_year=2024,
    )
    lib.add_book_to_library(b1)
    lib.add_book_to_library(b2)
    assert lib.get_total_book_count() == 2


def test_empty_library(lib: Library):
    lib.add_book_to_library(
        Book(
            title="Temp",
            authors=["X"],
            publisher="P",
            isbn="12",
            publication_year=2024,
        )
    )
    lib.empty_library()
    assert lib.get_total_book_count() == 0


def test_search_books(lib: Library):
    title = "Sapiens"
    lib.add_book_to_library(
        Book(
            title=title,
            authors=["Yuval Noah Harari"],
            publisher="Harper",
            isbn="9780062316097",
            publication_year=2011,
        )
    )
    hits = lib.search_books("sapiens")
    assert hits and hits[0].title == title


def test_get_all_books(lib: Library):
    titles = ["A", "B"]
    for t in titles:
        lib.add_book_to_library(
            Book(
                title=t,
                authors=["X"],
                publisher="P",
                isbn=t,
                publication_year=2024,
            )
        )
    retrieved = lib.get_all_books()
    got = [b["title"] for b in retrieved.values()]
    assert sorted(got) == sorted(titles)

def test_preseeded_data(tmp_path: Path):
    src = Path(__file__).with_name("test_database.json")
    db_file = tmp_path / "db.json"
    db_file.write_text(src.read_text())

    lib = Library(str(db_file))          # no empty_library()
    hits = lib.search_books("mockingbird")
    assert hits and hits[0].title == "To Kill a Mockingbird"
