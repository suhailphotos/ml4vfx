import uuid
from bookslib.book import Book


def test_uuid_is_unique() -> None:
    a = Book(
        title="Alpha",
        authors=["A"],
        publisher="P",
        isbn="1",
        publication_year=2024,
    )
    b = Book(
        title="Bravo",
        authors=["B"],
        publisher="P",
        isbn="2",
        publication_year=2024,
    )
    assert a.id != b.id and uuid.UUID(a.id) and uuid.UUID(b.id)


def test_authors_string() -> None:
    book = Book(
        title="Example",
        authors=["Foo", "Bar"],
        publisher="P",
        isbn="3",
        publication_year=2024,
    )
    assert book.authors_string == "Foo, Bar"


def test_search_string_contains_title() -> None:
    title = "UniqueTitle"
    book = Book(
        title=title,
        authors=["X"],
        publisher="P",
        isbn="4",
        publication_year=2024,
    )
    assert title.lower() in book.search_string
