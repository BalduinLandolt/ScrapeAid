"""
Launcher for the ScrapeAid application.

Run as __main__ to automatically launch the program.
"""

import bin.scraper as sc
import sys

print("Starting launcher")


def main():
    print("Launcher's main() method called.")
    scraper = sc.Scraper()
    print("Got Scraper: {}".format(scraper))

    if len(sys.argv) < 2:
        print("No Arguments handed over. Quiting.")
        quit(-1)

    arg = sys.argv[1]

    if arg.startswith("www.") or arg.startswith("http"):
        url = arg
        scraper.download_from_url(url)
        scraper.scrape_data_from_orig_to_textblocks()
        scraper.scrape_data_from_textblock_to_minimalist()
        scraper.scrape_minimalist_to_txt()
        print("Done.")
        quit(0)

    if arg == "from_orig":
        scraper.scrape_data_from_orig_to_textblocks()
        scraper.scrape_data_from_textblock_to_minimalist()
        scraper.scrape_minimalist_to_txt()
        print("Done.")
        quit(0)

    if arg == "from_textblock":
        scraper.scrape_data_from_textblock_to_minimalist()
        scraper.scrape_minimalist_to_txt()
        print("Done.")
        quit(0)

    if arg == "from_minimalist":
        scraper.scrape_minimalist_to_txt()
        print("Done.")
        quit(0)

    return


if __name__ == '__main__':
    main()
