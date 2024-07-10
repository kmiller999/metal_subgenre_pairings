# %% [markdown]
# ---
# title: Web Scraping Encyclopaedia Metallum
# author: Kevin Miller
# date: 2024/07/10
# output: html_document
# categories: [Python, Web Scraping]
# description: A web scraper designed to gather entries on hundreds of thousands of Metal bands. 
# ---

# %% [markdown]
"""
Note: This is an adapted version of the original Python script optimized for Quarto. 

Accordingly, the number of bands exported from this file to `metallum_bands.db` or `metallum_bands.csv` may not align perfectly with those shown in subsequent analyses. 
"""

# %%
# import necessary libraries
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
import time

# %%
# set options to fine-tune ChromeOptions()
options = ChromeOptions()
# run headless ChromeDriver to avoid popup
options.add_argument('--headless=new')

# instantiate Chrome driver with headless browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), 
                          options=options)

# define base url 
base_url = 'https://www.metal-archives.com/lists/'

# instantiate driver from base_url
driver.get(base_url)

# %%
# define function to extract band info from each individual page
def extract_band_info(page_source):
    # create BeautifulSoup object to parse HTMl aspects of page
    soup = BeautifulSoup(page_source, 'html.parser')
    # locate band info rows and select
    rows = soup.select('#bandListAlpha tbody tr')
    
    # create empty list to append data onto
    band_info = []
    
    # iterate through rows (bands) in page
    for row in rows:
        # define entry as dictionary that gets only text aspects
        # nth preserves increasing tr[] object
        entry = {
            'band_name': row.select_one('td:nth-of-type(1) a').text.strip(),
            'country': row.select_one('td:nth-of-type(2)').text.strip(),
            'genre': row.select_one('td:nth-of-type(3)').text.strip(),
            'status': row.select_one('td:nth-of-type(4) span').text.strip()
        }
        # append band_info with each entry
        band_info.append(entry)
        # return the final band_info
    return band_info

# %%
# define function to extract all bands from letter
def extract_bands_from_letter(page_source):
    # create empty list for all bands in each letter
    entire_letter_bands = []
    # set page_source equal to the driver's page_source
    page_source = driver.page_source
    # call extract_band_info function on each page and add on to entire_letter_bands
    entire_letter_bands.extend(extract_band_info(page_source=page_source))

    # instantiate logic
    while True:
        try:
            # define the next button 
            next_button = driver.find_element(By.XPATH, '//*[@id="bandListAlpha_next"]')
            # if on last page (no next_button), break
            if 'next paginate_button paginate_button_disabled' in next_button.get_attribute('class'):
                break 
            # otherwise, click to next page
            else: 
                next_button.click()
                # give content a second to load
                time.sleep(2)
                # define page_source as the driver's page_source
                page_source = driver.page_source
                # recall extract_band_info function as long as still on same letter
                entire_letter_bands.extend(extract_band_info(page_source=page_source))
                # add logic to print exception and break
        except Exception as e:
            print(f"Error: {e}")
            break
        # return all bands from the letter
    return entire_letter_bands

# %%
# define function to get every band on metallum
def extract_all_letters(base_url):
    # define base url
    base_url = base_url
    # define letter list
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # define character list (NBR would have been evaluated as 'N', 'B', and 'R')
    characters = ['NBR', '~']
    # set letters_finished (loop-breaking arg) to False
    letters_finished = False
    # set characters_finished (loop-breaking arg) to False
    characters_finished = False
    # create empty list for all bands
    all_bands = []
    
    # loop through list of letters
    for letter in letters:
        # unless already looped through, then break
        if letters_finished:
            break
        try:
            # set letter_page as base_url plus the letter
            letter_page = f"{base_url}{letter}"
            # print the url to monitor progress
            print(f"Accessing URL: {letter_page}")
            # get driver to access the letter page
            driver.get(letter_page)
            # give it 10 if it needs it
            driver.implicitly_wait(10)
            # extract the bands in each letter using previous function
            bands_in_letter = extract_bands_from_letter(driver.page_source)
            # add entries to all_bands
            all_bands.extend(bands_in_letter)
            # if letter is Z (end reached), set loop to break
            if letter == 'Z':
                letters_finished = True
                # print any exceptions
        except Exception as e:
            print(f"Error accessing {letter_page}: {e}")
            continue
        
    # character function is identical, but loops over the characters instead
    for character in characters:
        if characters_finished:
            break
        try:
            # set character_page as base_url plus the character
            character_page = f"{base_url}{character}"
            # print the url to monitor progress
            print(f"Accessing URL: {character_page}")
            # get driver to access the character page
            driver.get(character_page)
            # give it 10 if it needs it
            driver.implicitly_wait(10)
            # extract the bands in each character using previous function
            bands_in_character = extract_bands_from_letter(driver.page_source)
            # add entries to all_bands
            all_bands.extend(bands_in_character)
            # if character is ~ (end reached), set loop to break 
            if character == '~':
                characters_finished = True
                # print any exceptions
        except Exception as e:
            print(f"Error accessing {character_page}: {e}")
            continue    
        
        # return all the bands from all the letters and characters
    return all_bands 

# %%
# using extract_all_letters, save all bands to all_bands
all_bands = extract_all_letters(base_url=base_url)

# %%
# quit driver
driver.quit()

# %%
# convert all_bands to df
metallum_df = pd.DataFrame.from_dict(all_bands)

# create band_id column from index
metallum_df['band_id'] = metallum_df.index

# output df to csv
metallum_df.to_csv('data/metallum_bands.csv')

# %%
# import sqlite and create database 'metallum_bands.db'
import sqlite3

conn = sqlite3.connect('metallum_bands.db')

# add metallum_df to database
metallum_df.to_sql('metal_archives_table', con=conn, if_exists='replace', index=False)

# %%
# commit database changes and close sqlite connection
conn.commit()
conn.close()
