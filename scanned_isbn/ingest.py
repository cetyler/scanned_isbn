import duckdb
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngest:
    authors_file: Path = Path.cwd() / "data" / "authors.csv"
    editions_file: Path = Path.cwd() / "data" / "editions.csv"
    output_file: Path = Path.cwd() / "data" / "openlibrary.duckdb"
    scanned_isbn_file: Path = Path.cwd() / "data" / "openlibrary.duckdb"
    max_line_size: int = 10000000

    def initialize_db(self):
        self.connection = duckdb.connect(database = f"{self.output_file}")
    def drop_table(self, table_name):
        self.connection.sql(f"drop table if exists {table_name};")
    def load_authors(self) -> None:
        self.connection.sql(f"""
                   create table authors as
                    select column1[10:] as author_id
                          ,column3 as created
                          ,json_extract_string(column4, '$.name') as name
                          ,json_extract_string(column4, '$.personal_name') as personal_name
                          ,json_extract_string(column4, '$.alternate_names') as alternate_names
                          ,json_extract_string(column4, '$.bio') as bio
                          ,json_extract_string(column4, '$.location') as location
                          ,json_extract_string(column4, '$.birth_date') as birth_date
                          ,json_extract_string(column4, '$.death_date') as death_date
                          ,json_extract_string(column4, '$.date') as date
                          ,json_extract_string(column4, '$.links') as links
                      from (select *
                          from read_csv(f'{self.authors_file}', max_line_size=self.max_line_size)
                          );)
    """)

    def load_editions(self) -> None:
        self.connection.sql(f"""
        create table editions as
select column1[8:] as book_id
      ,column3 as created
      ,json_extract_string(column4, '$.title') as title
      ,json_extract_string(column4, '$.subtitle') as subtitle
      ,json_extract(column4, '$.other_titles') as other_titles
      ,json_extract(column4, '$.authors') as authors
      ,json_extract_string(column4, '$.publish_date') as publish_date
      ,json_extract_string(column4, '$.copyright_date') as copyright_date
      ,json_extract_string(column4, '$.edition_name') as edition_name
      ,json_extract_string(column4, '$.description') as description
      ,json_extract_string(column4, '$.notes') as notes
      ,json_extract(column4, '$.genres') as genres
      ,json_extract(column4, '$.table_of_contents') as table_of_contents
      ,json_extract(column4, '$.work_titles') as work_titles
      ,json_extract(column4, '$.series') as series
      ,json_extract_string(column4, '$.number_of_pages') as number_of_pages
      ,json_extract(column4, '$.subjects') as subjects
      ,json_extract(column4, '$.publishers') as publishers
      ,json_extract(column4, '$.collections') as collections
      ,json_extract(column4, '$.works') as works
      ,json_extract(column4, '$.volumes') as volumes
      ,json_extract(column4, '$.isbn_13') as isbn_13
      ,json_extract(column4, '$.isbn_10') as isbn_10
  from (select *
      from read_csv(f'{self.editions_file}', max_line_size=self.max_line_size)
      );
        """)

    def create_personal_library(self):
        self.connection.sql(f"""
        create table library (
         entry timestamptz default now()
        ,location text
        ,barcode text
        ,ownership_status text
        ,comment text
        ,primary key(barcode)
        );
        """)

    def update_personal_library(self):
        self.connection.sql(f"""
        insert or replace into library (entry, location, barcode, ownership_status, comment)
          select current_timestamp
                ,location
                ,barcode
                ,status
                ,comment
            from read_csv('{self.scanned_isbn_file}')
        order by current_timestamp;
        """
        )


        
