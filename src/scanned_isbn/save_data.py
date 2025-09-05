from .ingest import DataIngest
import click
from pathlib import Path
from trogon import tui
import sys

@tui()
@click.command()
@click.argument("data_type",
                type=click.Choice(["authors","editions","library"]),
                # help="Note that library is your personal library.",
                )
@click.argument('input_file',
              type=click.Path(exists=True),
              # help="The input file should match the type of data being inserted.",
              )
@click.argument('output_file',
              default=Path.cwd() / "data" / "openlibrary.duckdb",
              type=click.Path(exists=True),
              # help="The database to save the data to.",
              )
@click.option("--initialize",
                is_flag=True,
                help="Will drop any existing table selected and create new table.",
                )
def main(data_type: str, input_file: Path, output_file: Path, initialize: bool) -> None:
    data = DataIngest(
        output_file = output_file
        )
    data.initialize_db()

    if (data_type != "library") & (initialize is False):
        print(f"{data_type} requires to delete existing data. Use --initialize.")

    if initialize:
        data.drop_table(data_type)
        if data_type == "library":
            data.create_personal_library()


    if data_type == "authors":
        data.authors_file = input_file
        data.load_authors()
    elif data_type == "editions":
        data.editions_file = input_file
        data.load_editions()
    elif data_type == "library":
        data.scanned_isbn_file = input_file
        data.update_personal_library()
    else:
        print(f"{data_type} is not implemented.")
        sys.exit()

