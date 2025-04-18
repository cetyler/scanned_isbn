# Initial Requirements

This will be a simplified requirements document.

## Data Ingest

The data will be a CSV file.
The initial columns will be the following:

- Current Timestamp
  - The date and time when the scanned was performed.
- Location
  - Where the book is currently at.
- Barcode
  - The ISBN barcode.
- Status
  - Whether the book was purchased or rented.
- Comment
  - Freeform text to enter any additional information.

## Open Library

It doesn't appear that there are limits to their API.
At https://openlibrary.org/developers/dumps, it appears that you can download
the existing data.
Their API info located https://openlibrary.org/developers/api can be returned as
JSON.
The goal is to use their information to get the minimum information for each book:

- Title
- Author
- Publish date
- Number of pages
- Subjects

## Interface

The interface should be able to do the following:

- Add a book by using ISBN barcode.
- Search existing book in our library.
- Update info of an existing book in our library.

### Add Book

Initially by ISBN barcode.
The info to add should be similar to the the information in the CSV file from
the Apple Shortcut.
Optionally there should be a way to add a book by title and author as well.

### Search Existing Book

Should be able to search a book by title, author or barcode.
The results should be the available information of that book from the CSV file
and from Open Library.
There should be a way to denote whether the data needs updating.

### Update Info of a Book

This will be from searching.
Updating will update the timestamp and there should be able to update any info
from the CSV file.
If any of the Open Library data needs updating, this will be by checking the
API for updated information.

## Tests

For the initial release it is not required for full testing.
However there should be some basic testing to ensure that critical functionality
works.
