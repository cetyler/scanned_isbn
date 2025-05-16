# Initial Design

The initial design will make as much use of Python as possible.
While the goal is to create a Python package, the initial release it is not
required.
It can be separate scripts for data ingest for the CSV, data ingest for Open
Library and for the interface.

The goal of this program is to be a useful learning tool.
The longer design goal is to create a package that will go on PyPi.

## Data Ingest

The data will be saved in PostgreSQL.
However will use DuckDB as the interface to PostgreSQL.
The connection string will be as an input for now.

The CSV file will be saved into PostgreSQL as `scanned_isbn` and that table will
essentially have the same columns as the CSV file though there will be an
additional entered and modified timestamp columns.
Any existing data will get updated/replaced.

The CSV file is actually formatted using `;` instead of `,`.

**Note** using DuckDB it may actually be possible to not to use Python at all
and just be a simple DuckDB SQL script.

## Open Library

The initial design will not pull any data from Open Library for now.
Instead, will download ~16GB dump of their data and put that into PostgreSQL.
In the future will look at what is already in PostgreSQL and if the ISBN is not
there, then will go using the API.
The schema definition is located
https://github.com/internetarchive/openlibrary-client/tree/master/olclient/schemata.
Open Library already have tools to import this data into PostgreSQL located
https://github.com/LibrariesHacked/openlibrary-search so I will make use of
their tools.

If this is doesn't work, the fallback will be to just use the API calls since we
don't have that many books.

### API Call

Will use Open Library API calls for barcode and authors to be able to get the
minimum information.
There will be separate tables for books and authors.
There will also be a separate table to record the full JSON with the intend for
debugging purposes.

Similar to the data ingest, the initial intent is to use DuckDB to make the API
calls with a fullback to using Python requests library.

Similar to the Data Ingest, it should be possible to do all of this in DuckDB
and may not require Python either.

## Interface

This will be initially in Python.
Will see if I can use https://github.com/Textualize/textual-web so that it can
be used with mobile devices.
The fallback will be to use https://github.com/Textualize/trogon for the initial
interface.

The initial release will be to search for books only.
The search will either be by location (which will return all books for that
location), author (all books by that author), title (a simple fuzzy search) and
ISBN barcode.

The results will be returned as a simple table to combine the CSV file and Open
Library data.

## Tests

Will use `pytest` for all the testing.
Will create a set of test data and use that to verify basic operation of the API
calls, reading data and inserting data.
