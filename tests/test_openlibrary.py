import pytest
from scanned_isbn.openlibrary import OpenLibrary
from pathlib import Path

library_db = Path.cwd() / "data" / "openlibrary.db"
library = OpenLibrary(library_db)
library.initialize_db()

def test_search_by_isbn():
    isbn = 9780890090572
    good_author = "Arthur Conan Doyle"
    good_title = "The Original Illustrated Sherlock Holmes"

    book = library.search_by_isbn(isbn)

    assert book.fetchall()[0][0] == good_title
    assert book.fetchall()[0][1] == good_author

@pytest.mark.skip(reason="Right now it is very slow to search by author.")
def test_search_by_title():
    title = "The Original Illustrated Sherlock Holmes"
    good_author = "Arthur Conan Doyle"

    book = library.search_by_title(title)

    assert book.fetchall()[0][1] == good_author

def test_search_by_author():
    author = "Martha Wells"
    number_of_books = 11

    books = library.search_by_author(author)

    len(books) == number_of_books



