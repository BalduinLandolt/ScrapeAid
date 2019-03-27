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

    url = ""
    if len(sys.argv) > 1:
        #TODO check if actually is a URL, otherwise do other stuff
        url = sys.argv[1]
        res = scraper.download_from_url(url)
    else:
        print("No URL handed over. Working from Cache.")
        # TODO load from cache here

    scraper.scrape_cached_data()

    print("\nFinished with exit code: {}".format(res))
    return


if __name__ == '__main__':
    main()
