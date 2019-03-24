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
        url = sys.argv[1]
    else:
        print("No URL handed over. Exiting.")
        quit(-1)
    res = scraper.run(url)

    print("\nFinished with exit code: {}".format(res))
    return


if __name__ == '__main__':
    main()
