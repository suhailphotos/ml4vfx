# src/utils.py

"""
Utility helpers for booksLib. Gives us an easy place to add more helpers later
(e.g. timestamp generators, slugifiers, etc.).
"""
import uuid

class LibraryUtils:
    """
    Lightweight utility namespace for *booksLib*.
    - **Purpose**  Generate unique, collision-resistant IDs for books (or
        any other future library assets) using ``uuid.uuid4()``.
    - **Why UUID4?**  It’s fully random, RFC-4122 compliant, JSON-safe
    """

    @staticmethod
    def generate_book_uuid() -> str:
        """
        Return a fresh RFC-4122 UUID (version 4) as a string.

        Example
        -------
        >>> LibraryUtils.generate_book_uuid()
        '6f1a4b4e-3c9d-4e2c-bc7b-4b3d9e8f1c2a'
        """
        return str(uuid.uuid4())

if __name__ == "__main__":
    # generate a UUID
    uuid_str = LibraryUtils.generate_book_uuid()
    print(f"Generated UUID: {uuid_str}")

