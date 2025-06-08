import duckdb
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class OpenLibrary:
    input_file: Path
    connection: Any = None

    def initialize_db(self):
        self.connection = duckdb.connect(database = f"{self.input_file}", read_only=True)

    def search_by_isbn(self, isbn:str) -> dict[str, Any]:
        """
        Search for a book by ISBN.
        :param isbn:
        :return:
        """

        results = self.connection.sql(f"""
        select e.title
              ,a.name as author
              ,e.publish_date
              ,e.description
              ,e.series
              ,e.number_of_pages
              ,e.subjects
              ,a.bio
              ,a.birth_date
              ,a.death_date
              ,a.links
          from editions as e
          left join authors as a
          on a.author_id in e.authors
          where '{isbn}' in isbn_13 or '{isbn}' in isbn_10;
""")
        return results

    def search_by_title(self, title:str) -> dict[str, Any]:
        results = self.connection.sql(f"""
                select e.title
                      ,a.name as author
                      ,e.publish_date
                      ,e.description
                      ,e.series
                      ,e.number_of_pages
                      ,e.subjects
                      ,a.bio
                      ,a.birth_date
                      ,a.death_date
                      ,a.links
                  from editions as e
                  left join authors as a
                  on a.author_id in e.authors
                  where '{title}' ilike '%{title}%';
        """)
        return results


    def search_by_author(self, author:str) -> dict[str, Any]:
        results = self.connection.sql(f"""
                select distinct e.title
                      ,a.name as author
                      ,e.publish_date
                      ,e.description
                      ,e.series
                      ,e.number_of_pages
                      ,e.subjects
                      ,a.bio
                      ,a.birth_date
                      ,a.death_date
                      ,a.links
                  from editions as e
                  left join authors as a
                  on a.author_id in e.authors
                  where a.name ilike '{author}'
                  order by e.publish_date desc;
        """)
        return results




