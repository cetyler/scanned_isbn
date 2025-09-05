import pytest
from scanned_isbn.ingest import DataIngest
from pathlib import Path 
import csv
import datetime


def convert(date_time):
    format = '%Y-%m-%dT%H:%M:%S%z'
    datetime_str = datetime.datetime.strptime(date_time, format)
    
    return datetime_str.replace(tzinfo=None) + datetime.timedelta(hours=5) # remove timezone and add offset

def test_load(tmp_path):
    scanned_isbn_file = Path.cwd() / 'data' / 'scanned_isbn.csv'
    authors_file = Path.cwd() / 'data' / 'authors.csv'
    output_file = tmp_path / 'output.duckdb'
    editions_file = Path.cwd() / 'data' / 'editions.csv'

    good_data = list()

    with open(scanned_isbn_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            row_value = list()
            for value in row:
                try:
                    value = convert(value)
                except:
                    pass
                if value == '':
                    row_value.append(None)
                else:
                    row_value.append(value)
            good_data.append(tuple(row_value))


    data = DataIngest(
        scanned_isbn_file=scanned_isbn_file,
        authors_file=authors_file,
        output_file=output_file,
        editions_file=editions_file,
    )

    data.initialize_db()
    data.create_personal_library()
    data.update_personal_library()


    assert data.connection.sql("select count(*) from library;").fetchone()[0] > 0
    current_library = data.connection.sql("""
                                select entry::timestamp as entry
                                      ,location
                                      ,barcode
                                      ,ownership_status
                                      ,comment
                                  from library;
                               """).fetchall() 

    #assert current_library[0] == good_data[0]
    assert len(good_data) == 27 # There are duplicates
    assert len(current_library) == 24 # No duplicates should be there


