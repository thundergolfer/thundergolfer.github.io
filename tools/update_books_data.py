"""
The purpose of this script is to update the /_data/books.yaml file that is used to build
the /library page of the website.
"""

import csv
import json
import pathlib
import re
import subprocess

from typing import Optional

#  I'll leave out children's authors, young-adult fiction, and bland fiction from what shows up on my website
IGNORED_AUTHORS = {
    "J.K. Rowling",  # Children's author
    "Garth Nix",  # Children's author
    "Lemony Snicket",  # Children's author
    "Jeffrey Archer",  # Meh
    "Matthew Reilly",  # Young Adult
    "Andy McNab",  # Meh
    "Dan Brown",  # Meh / Pop-Fiction
    "Neil Strauss",  # Eugh, bit gross
    "Christopher Paolini",  # Young Adult
    "Jeremy Clarkson",  # Blurgh
}

# For some reason Goodreads left out ISBN information for some of the books in my collection,
# even though the ISBN info is available in Goodreads if you look up the data on their website.
TITLE_TO_ISBN = {
    "China in Ten Words": "9780307739797",
    "Priestdaddy": "9780399573262",
    "The Man in the High Castle": "9780141186672",
    "A Children's Bible": "9781324005032",
    "When We Cease to Understand the World": "9781681375663",
    "Operating Systems: Three Easy Pieces": "9781985086593",
    "The Rust Programming Language": "9781593278281",
    "The Glass Teat": "9780759230309",
    "A Farewell to Arms": "9780684174693",
    "Public Citizens: The Attack on Big Government and the Remaking of American Liberalism": "",
    "Losing the Signal: The Untold Story Behind the Extraordinary Rise and Spectacular Fall of BlackBerry": "9781443436182",
    "A Cyborg Manifesto: Science, Technology, and Socialist-Feminism in the Late Twentieth Century": "9788807460012",
    "For Whom the Bell Tolls": "1439571481",
    "A Moveable Feast": "0684833638",
    "The New Jim Crow: Mass Incarceration in the Age of Colorblindness": "1620975459",
    "Snow Crash": "8496208621",
    "Ishmael": "0553375407",
    "Power Without Glory": "9780207147241",
    "The Federalist Papers": "9780143121978",
    "The Autobiography of Malcolm X": "9780345350688",
    "My Brilliant Friend": "9781609450786",
    "The Left Hand of Darkness (Hainish Cycle, #4)": "9780441478125",
    "Neuromancer (Sprawl, #1)": "0441569595",
    "The End of Policing": "9781784782924",
    "The Sirens of Titan": "9780385333498",
    "Entitled: How Male Privilege Hurts Women": "9780141990743",
    "Skunk Works: A Personal Memoir of My Years at Lockheed": "0751515035",
    "Designing Data-Intensive Applications": "9781449373320",
    "Dark Money: The Hidden History of the Billionaires Behind the Rise of the Radical Right": "9780385535601",
    "Bit Tyrants: The Political Economy of Silicon Valley": "9781642590319",
    "Creating a Learning Society: A New Approach to Growth, Development, and Social Progress": "9780231175494",
    "New Dark Age: Technology and the End of the Future": "9781786635471",
    "The Restaurant at the End of the Universe (Hitchhiker's Guide to the Galaxy, #2)": "9780671442682",
    "The Handmaid's Tale (The Handmaid's Tale, #1)": "9780449212608",
    "The Trial": "9781529021073",
    "The Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1)": "9780434023394",
    # NOTE: The ISBN is actually for 'Orwell's England'. 'Road to Wigan Pier' does have a cover in Open Cover
    "The Road to Wigan Pier": "0141185171",
    # Analogie is missing its ISBN.
    "When Breath Becomes Air": "9780812988406",
    "The Defining Decade: Why Your Twenties Matter—And How to Make the Most of Them Now": "",
    #     Digital Fortress is missing its ISBN.
    #     The Da Vinci Code (Robert Langdon, #2) is missing its ISBN.
    #                               The Elements of Style is missing its ISBN.
    "1984": "9780141036144",
    "To Kill a Mockingbird": "9781784752637",
    "The Great Gatsby": "9781839407598",
    "The Return of the King (The Lord of the Rings, #3)": "9782266120975",
    # Harry Potter and the Goblet of Fire (Harry Potter, #4) is missing its ISBN.
    # Harry Potter and the Deathly Hallows (Harry Potter, #7) is missing its ISBN.
    # Harry Potter and the Sorcerer's Stone (Harry Potter, #1) is missing its ISBN.
    "Walden": "9781722500030",
    "How to Win Friends and Influence People": "0671355007",
    "Treasure Islands: Uncovering the Damage of Offshore Banking and Tax Havens": "9781847921109",
    "The Shark Net": "0670888095",
    "Chaos Monkeys: Obscene Fortune and Random Failure in Silicon Valley": "9780062458209",
    "Dune Messiah (Dune Chronicles, #2)": "9780425035856",
    "Why We're Polarized": "9781476700366",
    "The Pearl": "9782070364282",
    "Friday Black": "1787476014",
    "The New New Thing: A Silicon Valley Story": "9781469244341",
    "The Big Short: Inside the Doomsday Machine": "9780393072235",
    "Gorgias": "0140440941",
    "Flowers for Algernon": "9781474605731",
    "The Nickel Boys": "0345804341",
    "Little Women": "9780451529305",
    "The Dispossessed (Hainish Cycle, #6)": "9781857988826",
    "Snow Crash": "9780241953181",
    "An Elegant Puzzle: Systems of Engineering Management": "9781732265189",
    "The Medium is the Message": "9781584230700",
    "The Song of Achilles": "9781408821985",
    "Team of Rivals: The Political Genius of Abraham Lincoln": "9780141043722",
    "Wage Labour and Capital": "9780717804702",
    "Cryptonomicon": "9780380973460",
    "The Phoenix Project: A Novel About IT, DevOps, and Helping Your Business Win": "9781942788300",
    "Draft No. 4: On the Writing Process": "9780374537975",
    "The Doors of Perception": "9780060801717",
    "The Little Prince": "9780156012195",
    "Do Androids Dream of Electric Sheep?": "9780575094185",
    "Tender Is the Night": "9780684801544",
    "Between the World and Me": "9780812993547",
    "No One Is Talking About This": "9780593332542",
    "God Bless You, Mr. Rosewater": "9780440129295",
}

# Goodreads didn't allow 1/2 stars in ratings annoyingly, but I want to try them.
RATING_OVERRIDES = {
    "Notes on Nationalism": "3.5",
    "The Return of the King (The Lord of the Rings, #3)": "4.5",
    "The New New Thing: A Silicon Valley Story": "3.5",
    "I Am a Strange Loop": "4.5",
    "Why Knowledge Matters: Rescuing Our Children from Failed Educational Theories": "4.5",
    "Flowers for Algernon": "4.5",
    "Neuromancer (Sprawl, #1)": "5",
    "Working in Public: The Making and Maintenance of Open Source Software": "3",
}


def fmt_rating(rating: str):
    if not rating:
        return "🤷‍♂️"
    rating = float(rating)
    if rating % 1 != 0:
        return ("★" * int(rating)) + "☆"
    return "★" * int(rating)


def get_book_review_path(book_reviews_directory: pathlib.Path, title: str, author: str) -> Optional[str]:
    cleaned_title = "-".join(re.sub("[!'.:]", "", title).split()).lower()
    cleaned_author = "-".join(re.sub("[!'.:]", "", author).split()).lower()
    expected_review_filename = f"{cleaned_title}-{cleaned_author}.md"
    expected_review_path = book_reviews_directory / expected_review_filename
    print(expected_review_path)
    if expected_review_path.exists():
        return f"{cleaned_title}-{cleaned_author}/"
    return None


if __name__ == "__main__":
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8").strip()

    book_reviews_directory = pathlib.Path(repo_root, "collections", "_reviews")
    reading_data_csv_path = pathlib.Path(repo_root, "_data", "goodreads_library_export.csv")

    entries = []
    with open(reading_data_csv_path, newline="") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in spamreader:
            entries.append(row)

    library_data = []
    antilibrary_data = []
    for row in entries:
        read_count = int(row["Read Count"])
        # TITLE_TO_ISBN takes precedence because some of the ISBNs in Goodreads data don't have cover available
        isbn = TITLE_TO_ISBN.get(row["Title"]) or row["ISBN"][2:-1] or row["ISBN13"][2:-1]
        review_path = get_book_review_path(
            book_reviews_directory=book_reviews_directory,
            title=row["Title"],
            author=row["Author"]
        )
        if review_path == "neal-stephenson":
            raise RuntimeError("what")
        entry = {
            "title": row["Title"],
            "author": row["Author"],
            "rating": fmt_rating(RATING_OVERRIDES[row["Title"]]) if RATING_OVERRIDES.get(row["Title"]) else fmt_rating(row["My Rating"]),
            "isbn": isbn,
            "review_path": review_path,
            "year_i_finished_reading": row["Date Read"].split("/")[0] if row["Date Read"] else None,
        }

        if not isbn:
            print(entry["title"] + " is missing its ISBN.")

        passes_filters = (
                entry["author"] not in IGNORED_AUTHORS
        )
        if not passes_filters:
            continue

        have_read = (
            # All books I've at least started will pass this filter
            read_count > 0 and
            # only books that I've finished reading show up on this shelf in Goodreads
            row["Exclusive Shelf"] == "read"
        )
        if have_read:
            library_data.append(entry)
        else:
            antilibrary_data.append(entry)

    library_data_output_path = pathlib.Path(repo_root, "_data", "library.yaml")
    with open(library_data_output_path, "w") as f:
        json.dump(library_data, f, indent=4)

    antilibrary_data_output_path = pathlib.Path(repo_root, "_data", "antilibrary.yaml")
    with open(antilibrary_data_output_path, "w") as f:
        json.dump(antilibrary_data, f, indent=4)
