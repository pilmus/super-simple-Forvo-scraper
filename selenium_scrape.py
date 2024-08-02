import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')
wordlistfile = os.getenv('WORD_LIST')
download_dir = os.getenv('DOWNLOAD_DIR')
lang = os.getenv('LANG')


base_url = f"https://apifree.forvo.com/action/word-pronunciations/format/json/word/QUERY/language/{lang}/key/{api_key}/"


reverse_wordlist = []
try:
    driver = webdriver.Firefox()
    with open (wordlistfile,'r',encoding='utf-8') as fp:
        words = fp.read().splitlines()

        for word in words:
            url = base_url.replace('QUERY', word)
            
            driver.get(url)
            
            try:
                sound_file = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#\/items\/0\/pathmp3 > .treeValueCell a")))
                
                sound_file.click()
                reverse_wordlist.append(word)

            except (NoSuchElementException, StaleElementReferenceException):
                print(f'{word} not found.')
            sleep(1)
except Exception as e:
    print(e)
finally:            
    driver.quit()

reverse_wordlist = reversed(reverse_wordlist)

downloaded_files = os.listdir(download_dir)
downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir,x)),reverse=True)

for word,old_filename in zip(reverse_wordlist, downloaded_files):
    new_filename = f"{word}.mp3"
    new_filename_path = os.path.join(download_dir,new_filename)
    old_filename_path = os.path.join(download_dir,old_filename)
    
    if os.path.exists(new_filename_path):
        os.remove(new_filename_path)
    os.rename(old_filename_path,new_filename_path)



# 




# - go through list of words and download them with the selenium script
# -- if a word isn't found, remove it from the list (or don't prepend it to the reversed list i guess)
# - in reverse order, go through the words in the downloaded folder 
# -- rename them to the correct word