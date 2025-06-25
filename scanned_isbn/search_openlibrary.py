from .openlibrary import OpenLibrary
import click
from pathlib import Path
from trogon import tui

@tui()
@click.command()
@click.argument("search_type",
                type=click.Choice(["author","title","isbn"])
                )
@click.argument("search_entry")
@click.option('--input_file',
              default=Path.cwd() / "data" / "openlibrary.db",
              type=click.Path(exists=True),
              )
def main(search_type: str, search_entry: str, input_file: Path):
    book = None
    openlibrary = OpenLibrary(input_file=input_file)
    openlibrary.initialize_db()
    if search_type == "isbn":
        book = openlibrary.search_by_isbn(search_entry)
    elif search_type == "title":
        book = openlibrary.search_by_title(search_entry)
    elif search_type == "author":
        book = openlibrary.search_by_author(search_entry)
    else:
        print("Unknown search type")


    book.show()
