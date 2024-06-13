# Imports
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re

# Set up web driver
driver = Chrome()
driver.get('https://msumcmaster.ca/clubs/clubs-directory/') # Paste url of club directory here
email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # Regex to retrieve all email addresses 

try:
    # For campuslabs sites only - click through every "show more" button
	while driver.find_element(By.CSS_SELECTOR, 'button[tabindex="0"][type="button"]').is_displayed():
          driver.find_element(By.CSS_SELECTOR, 'button[tabindex="0"][type="button"]').click()
except:
     print()
finally:
    # Extract all hyperlinks from the directory page
    elems = driver.find_elements(by=By.XPATH, value="//a[@href]")
    links = [] # declare a list to store the extracted urls

    # Stores urls in an array
    for elem in elems:
        link = elem.get_attribute("href")
        if "initiative" in link or "organization" in link or "organisation" in link: # Filters relevent links that contain keywords initiative/organisation/prganization
            links.append(link) 

    # Traverse the page of each club to find the name and email
    for i in links:
        try:
            print(i)
            driver.get(i) # Enter the page of the club

            # Retrieve all text stored inside an h1 tag to find the club name
            headings = driver.find_elements(By.TAG_NAME, 'h1')
            for i in headings:
                print(i.get_attribute('textContent'))
            
            # Retrieve all email addresses on the page to find the club email
            possibleEmails = driver.find_elements(By.XPATH, "//*[contains(text(), '@') or contains(@href, 'mailto:')]")
            emails = []
            for j in possibleEmails:
                text = j.text
                href = j.get_attribute('href')
                if not text: # If j.text cannot retrieve the text, use the get_attribute function
                    text = j.get_attribute('textContent')
                if text:
                    result = re.findall(email_regex, text) # Filter possibleEmails using the regex
                    if len(result) > 0:
                        emails = re.findall(email_regex, text)
                elif href and href.startswith('mailto:'): # Filter possibleEmails by checking if the href begins with mailto
                    emails = re.findall(email_regex, href)
            for e in emails:
                print(e)
            print("")
        except:
            print("There was an error accessing this page.")
