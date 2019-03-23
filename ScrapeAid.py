"""
Launcher for the ScrapeAid application.

Run as __main__ to automatically launch the program.
"""

import bin.scraper as sc

print("Starting launcher")


def main():
    print("Launcher's main() method called.")
    scraper = sc.Scraper()
    print("Got Scraper: {}".format(scraper))
    res = scraper.run()

    print("\nFinished with exit code: {}".format(res))
    return


if __name__ == '__main__':
    main()
