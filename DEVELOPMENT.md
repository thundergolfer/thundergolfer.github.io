## Development Documentation

This information is only really useful for the site owner.

### Build, Test, Local-Dev

#### Install

`bundle install`

#### Run Locally

`bundle exec jekyll server`

### Library/Anti-Library

#### Updating Book Data

The library and anti-library pages are powered by data files:
- `_data/library.yaml` - Books you've read
- `_data/antilibrary.yaml` - Books you want to read

To update these files, run:

```bash
python3 tools/update_books_data.py
```

This script reads from `_data/goodreads_library_export.csv` and generates the library/antilibrary YAML files.

#### Book Covers

Book covers are pre-downloaded from OpenLibrary and stored locally in `/images/book-covers/` for faster loading and better CDN caching via Cloudflare.

**After updating library/antilibrary data**, download new book covers:

```bash
python3 tools/download_book_covers.py
```

This script:
- Reads ISBNs from `_data/library.yaml` and `_data/antilibrary.yaml`
- Downloads covers from OpenLibrary API to `/images/book-covers/{isbn}.jpg`
- Skips covers that already exist locally
- Reports success/failure statistics

**Fallback mechanism:**
1. Pages try to load local cover: `/images/book-covers/{isbn}.jpg`
2. If local cover fails, falls back to OpenLibrary: `http://covers.openlibrary.org/b/ISBN/{isbn}-L.jpg`
3. If OpenLibrary fails, JavaScript replaces with placeholder: `/images/placeholder-book-cover.png`

**Note:** Commit the downloaded covers to git so they're served via the CDN.
