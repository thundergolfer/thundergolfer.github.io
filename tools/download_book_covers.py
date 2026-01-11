"""
Download book covers from OpenLibrary for static serving.

This script reads ISBN data from library.yaml and antilibrary.yaml,
downloads the cover images from OpenLibrary, and saves them locally
to /images/book-covers/ for static serving via CDN.
"""

import json
import pathlib
import subprocess
import time
from typing import Dict, List, Set

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def setup_session() -> requests.Session:
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def load_book_data(data_path: pathlib.Path) -> List[Dict]:
    """Load book data from YAML file (actually JSON format)."""
    with open(data_path, 'r') as f:
        return json.load(f)


def download_cover(session: requests.Session, isbn: str, output_path: pathlib.Path) -> bool:
    """
    Download a book cover from OpenLibrary.
    
    Returns True if successful, False otherwise.
    """
    if not isbn:
        return False
    
    # Check if cover already exists
    if output_path.exists() and output_path.stat().st_size > 1024:
        return True
    
    url = f"http://covers.openlibrary.org/b/ISBN/{isbn}-L.jpg"
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        # Check if we got a valid image (OpenLibrary returns a 1x1 pixel for missing covers)
        if len(response.content) < 1024:  # Less than 1KB is likely the placeholder
            return False
        
        # Save the cover
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Failed to download cover for ISBN {isbn}: {e}")
        return False


def main():
    """Main function to download all book covers."""
    # Get repository root
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8").strip()
    
    repo_path = pathlib.Path(repo_root)
    
    # Set up paths
    library_path = repo_path / "_data" / "library.yaml"
    antilibrary_path = repo_path / "_data" / "antilibrary.yaml"
    covers_dir = repo_path / "images" / "book-covers"
    
    # Create covers directory if it doesn't exist
    covers_dir.mkdir(parents=True, exist_ok=True)
    
    # Load book data
    print("Loading book data...")
    library_books = load_book_data(library_path)
    antilibrary_books = load_book_data(antilibrary_path)
    all_books = library_books + antilibrary_books
    
    # Collect unique ISBNs
    isbns: Set[str] = set()
    for book in all_books:
        isbn = book.get("isbn", "")
        if isbn:
            isbns.add(isbn)
    
    print(f"Found {len(isbns)} unique ISBNs to process")
    print(f"Covers will be saved to: {covers_dir}")
    print()
    
    # Set up session
    session = setup_session()
    
    # Download covers
    successful = 0
    failed = 0
    skipped = 0
    
    for i, isbn in enumerate(sorted(isbns), 1):
        output_path = covers_dir / f"{isbn}.jpg"
        
        # Check if already exists
        if output_path.exists() and output_path.stat().st_size > 1024:
            print(f"[{i}/{len(isbns)}] ⊙ Skipping {isbn} (already exists)")
            skipped += 1
            continue
        
        print(f"[{i}/{len(isbns)}] Downloading {isbn}...", end=" ")
        
        if download_cover(session, isbn, output_path):
            print("✓")
            successful += 1
        else:
            print("✗ (no cover available)")
            failed += 1
        
        # Be nice to OpenLibrary - small delay between requests
        time.sleep(0.2)
    
    # Print summary
    print()
    print("=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total ISBNs:     {len(isbns)}")
    print(f"Successful:      {successful}")
    print(f"Failed/Missing:  {failed}")
    print(f"Already existed: {skipped}")
    print()
    print(f"Covers saved to: {covers_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()


