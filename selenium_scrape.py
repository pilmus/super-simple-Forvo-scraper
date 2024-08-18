import argparse
import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
base_url_str = f"https://apifree.forvo.com/action/word-pronunciations/format/json/word/QUERY/language/LANGUAGE_CODE/key/{api_key}/"


def download_words_in_file(wordlistfile: Path, base_url: str, dest_dir: Path):
    with open(wordlistfile, "r", encoding="utf-8") as fp:
        words = fp.read().splitlines()
    download_list_of_words(words, base_url, dest_dir)


def download_single_word(word: str, base_url: str, dest_dir: Path):
    download_list_of_words([word], base_url, dest_dir)


def download_list_of_words(words: list[str], base_url: str, dest_dir: Path):
    reverse_wordlist = []
    try:
        driver = webdriver.Firefox()
        for word in words:
            url = base_url.replace("QUERY", word)

            driver.get(url)

            try:
                sound_file = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#\/items\/0\/pathmp3 > .treeValueCell a")
                    )
                )

                sound_file.click()
                reverse_wordlist.append(word)

            except Exception:
                print(f"{word} not found.")
            sleep(1)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    reverse_wordlist = reversed(reverse_wordlist)

    downloaded_files = os.listdir(dest_dir)
    downloaded_files.sort(
        key=lambda x: os.path.getmtime(os.path.join(dest_dir, x)), reverse=True
    )

    for word, old_filename in zip(reverse_wordlist, downloaded_files):
        new_filename = f"{word}.mp3"
        new_filename_path = os.path.join(dest_dir, new_filename)
        old_filename_path = os.path.join(dest_dir, old_filename)

        if os.path.exists(new_filename_path):
            os.remove(new_filename_path)
        os.rename(old_filename_path, new_filename_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Forvo Word Downloader",
        description="Downloads a (list of) word(s) through the Forvo API, using Selenium.",
    )
    parser.add_argument(
        "-w",
        "--word-or-file",
        help="Either a single word or the path to a file with multiple words, one word per line.",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="Path to destination folder of the sound files.",
        required=True,
    )
    parser.add_argument(
        "-l", "--language", help="Forvo language code. Default: ko.", default="ko"
    )

    args = parser.parse_args()

    base_url = base_url_str.replace("LANGUAGE_CODE", args.language)
    destination_folder = Path(args.destination)
    word_or_file = args.word_or_file
    if os.path.isfile(word_or_file):
        download_words_in_file(Path(word_or_file), base_url, destination_folder)
    else:
        download_single_word(word_or_file, base_url, destination_folder)
