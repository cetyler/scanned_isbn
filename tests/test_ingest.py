import pytest
from scanned_isbn.ingest import DataIngest
from pathlib import Path 
import csv
import datetime


def convert(date_time):
    format = '%Y-%m-%dT%H:%M:%S%z'
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str.replace(tzinfo=None) + datetime.timedelta(hours=5) # remove timezone and add offset

def test_load():
    test_file = Path.cwd() / 'data' / 'scanned_isbn.csv'

    good_data = list()

    with open(test_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            row_value = list()
            for value in row:
                try:
                    value = convert(value)
                except:
                    pass
                try:
                    value = int(value)
                except:
                    pass
                if value == '':
                    row_value.append(None)
                else:
                    row_value.append(value)
            good_data.append(tuple(row_value))


    data = DataIngest(
        input_file=test_file,
    )

    data.initialize_db()
    data.load()

    assert data.connection.sql("select count(*) from input_data;").fetchone()[0] > 0
    assert data.connection.sql("select * from input_data;").fetchall() == good_data




