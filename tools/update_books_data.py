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
    "Entitled: How Male Privilege Hurts Women": "9781984826572",
    "Skunk Works: A Personal Memoir of My Years at Lockheed": "0751515035",
    "Designing Data-Intensive Applications": "9781449373320",
    "Dark Money: The Hidden History of the Billionaires Behind the Rise of the Radical Right": "9780385535601",
    "Bit Tyrants: The Political Economy of Silicon Valley": "9781642591798",
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
    "Flames": "9781786496294",
    "Shakespearean Tragedy": "9780230001893",
    "The Culture of Narcissism: American Life in An Age of Diminishing Expectations": "9780393307382",
    "A Man's Place": "0345378954",
    "Tinker, Tailor, Soldier, Spy (George Smiley, #5; Karla Trilogy, #1)": "9780143119784",
    # Cover-safe ISBN overrides verified after Goodreads export refresh.
    "The Great Divide: Australia's Housing Mess and How to Fix It (Quarterly Essay #92)": "9781760644239",
    "The Story of a New Name (Neapolitan Novels, #2)": "9781787535169",
    "Those Who Leave and Those Who Stay (Neapolitan Novels, #3)": "9781609452339",
    "My Brilliant Friend (Neapolitan Novels, #1)": "9781609459468",
    "Democracy in Chains: The Deep History of the Radical Right's Stealth Plan for America": "9781101980972",
    "God, Human, Animal, Machine: Technology, Metaphor, and the Search for Meaning": "9780525562719",
    "Data & Reality": "9781935504214",
    "Trust": "9780593420317",
    "This Side of Paradise": "9788420655642",
    "Lolita": "9789592540637",
    "How to Win Friends & Influence People": "9781442344839",
    "The Call of the Wild": "9781329820418",
    "The Dispossessed: An Ambiguous Utopia": "9788804689973",
    "The Left Hand of Darkness": "9788445070239",
    "The Medium is the Massage: An Inventory of Effects": "9781584230700",
    "The quiet revolution": "9780972330084",
    "Dune (Dune, #1)": "9780593438374",
    "Cat’s Cradle": "9780808520696",
    "The Restaurant at the End of the Universe (The Hitchhiker's Guide to the Galaxy, #2)": "9788599296950",
    "The Hitchhiker’s Guide to the Galaxy (The Hitchhiker's Guide to the Galaxy, #1)": "9780385365925",
    "The Defining Decade: Why Your Twenties Matter—And How to Make the Most of Them Now": "9780446561754",
    "The Consolations of Philosophy": "9780786167371",
    "Digital Fortress": "9787020048144",
    "The da Vinci Code (Robert Langdon, #2)": "9789170012945",
    "The Da Vinci Code (Robert Langdon, #2)": "9789170012945",
    "The Elements of Style": "9781794480025",
    "The Fountainhead": "9780451133199",
    "Romeo and Juliet": "9780497902209",
    "Infinite Jest": "9783499249570",
    "The Hobbit, or There and Back Again (The Lord of the Rings, #0)": "9780345445605",
    "The Hobbit, or There and Back Again": "9780345368584",
    "Walden or, Life in the Woods": "9780030093203",
    "Slaughterhouse-Five": "9780385333849",
    "The Perfectionists: How Precision Engineers Created the Modern World": "9780062931962",
    "The Emperor of All Maladies: A Biography of Cancer": "9781508279327",
    "Wolf Hall (Thomas Cromwell, #1)": "9781408461259",
    "The Bonfire of the Vanities": "9781433288432",
    "Red Dragon (Hannibal Lecter, #1)": "9780553227468",
    "Analogie: de kern van ons denken (Dutch Edition)": "9780465018475",
    "This is Going to Hurt: Secret Diaries of a Junior Doctor": "9781509899470",
    "The Fatal Shore: The Epic of Australia's Founding": "9780099448549",
    "High-Rise": "9781631492686",
    "Demon Copperhead": "9788248934721",
    "The Woman Destroyed": "9781299035515",
    "An Actor's Work": "9780203936153",
    "There Is No Antimemetics Division": "9781529953176",
    "K-punk: The Collected and Unpublished Writings of Mark Fisher": "9781912248285",
    "One Child: The Story of China's Most Radical Experiment": "9781515952435",
    "Anna Karenina": "9788497941648",
    "Pale Fire": "9782070383634",
    "The Brothers Karamazov": "9781731705525",
    "Industrial Society and Its Future": "9781726763714",
    "Myra Breckenridge/Myron": "9780525566502",
    "An Immense World: How Animal Senses Reveal the Hidden Realms Around Us": "9780593133231",
    "The Software Paradox": "9781491900932",
    "Container Security: Fundamental Technology Concepts that Protect Containerized Applications": "9781492056706",
    "The Bitcoin Standard: The Decentralized Alternative to Central Banking": "9781978651043",
    "T-SQL Querying": "9780735685048",
    "The Contrarian: Peter Thiel and Silicon Valley's Pursuit of Power": "9781984878533",
    "The Contrarian: Peter Thiel and the Rise of the Silicon Valley Oligarchs": "9781984878533",
    "A Wizard of Earthsea (Earthsea Cycle, #1)": "9780606005739",
    "Will There Ever Be Another You": "9780593718551",
    "Combat Liberalism": "9782758701057",
    "The Steppenwolf": "9780793533275",
    "Programming Languages: History and Fundamentals": "9780137299881",
    "Key Thinkers of the Radical Right: Behind the New Threat to Liberal Democracy": "0190877588",
    "Just Mercy": "9780812994537",
    "Why Socialism?": "9789724409450",
    "What Is to Be Done: political engagement and saving the planet": "9781913348038",
    "For Whom the Bell Tolls": "9788422610373",
    "Ishmael (Ishmael, #1)": "9780553078756",
    "The Unlucky Australians (Australian Aborigines)": "9780975770832",
    "The Abolition of Man": "9780020867906",
    "On Language: Chomsky's Classic Works Language and Responsibility and Reflections on Language in One Volume": "9781565844759",
    "Power Without Glory": "9780522848885",
    "Living": "9780002711845",
    "The Federalist Papers": "9781404302303",
    "Stranger in a Strange Land": "9780340938348",
    "As I Lay Dying": "9780606021715",
    "The Ministry for the Future": "9780316300148",
    "The Handmaid’s Tale (The Handmaid's Tale, #1)": "9783596259878",
    "Messengers of the Right: Conservative Media and the Transformation of American Politics": "9780812248395",
    "Crime and Punishment": "9781435131828",
    "Robinson Kruso": "9789754052510",
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
