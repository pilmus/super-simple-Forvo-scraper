# Forvo scraping with Selenium
This project was inspired by [forvo scraper example](https://github.com/NSBum/forvo_scraper_example).

I'll quote from their [README](https://github.com/NSBum/forvo_scraper_example/blob/main/README.md) their points on the ethics (So to speak) of scraping Forvo:

> - Forvo is an excellent resource for language learners and I wish the company the best of luck in commercializing word and phrase pronunciations. This code is not meant to deprive them of resources to further their misson.
> - They have an API that in principle should allow developers to access pronunciations. In fact, I'm a paid monthly subscriber to that API. But it is often very slow and frequently is down completely without any status information or response from the support staff.

## Why this scraper?
In an effort to understand the forvo scraper example code, I decided to start from the ground up with only the most basic elements I need for my own usecase.
 
What is does is:
- Open API link in the browser
- Find & click first link to a sound file
- Rename all downloaded sound files to the word they contain

## Usage

- Install `selenium` and `python-dotenv` (this is only necessary if you want to load your api key through a `.env` file. I only did this so I wouldn't put my own api key on GitHub.)
- Put the words you want in `wordlist.txt`.
- Copy `example.env` to `.env` and change the values.
- `python selenium_scrape.py`.

If you want to download 