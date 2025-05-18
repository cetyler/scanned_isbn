import duckdb
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngest:
    input_file: Path
    #output_file: Path

    def initialize_db(self):
        self.connection = duckdb.connect(database = ":memory:")
    def load(self):
        self.connection.sql(f"""
                   create table input_data as
                   select *
                   from read_csv('{self.input_file}')
    """)

        
