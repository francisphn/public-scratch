# Version 2.0

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # Depends on devices this may be needed
import time
import json
import os


driver = webdriver.Chrome("/home/cosc/student/hph44/Downloads/chromedriver")  # Change this directory


class WebScrape(object):
    """A class to scrape manually"""

    def __init__(self, link):
        self.link = link

        # Fetch raw dictionary data using command ROOT_QUERY
        # Also Find company name from website, using Selenium
        self.raw_dict_data, self.name = self.fetch()

        self.raw_string_data = self.dict_to_string()  # Convert it from dictionary to a raw string
        self.the_index = self.raw_string_data.find("\"ratings\": {")  # Find the index where the interested data sits
        self.extracted_string = self.extract()  # Extract information from that data
        self.data = self.make_dict()  # Assign information into a Python dictionary, with further extraction

    def fetch(self):
        # Open browser
        driver.get(self.link)
        time.sleep(1)

        # Execute this JavaScript script
        # which will return a JavaScript object, and in the process, also conveniently
        # converts it into a Python Dictionary
        fetched_dict = driver.execute_script("return appCache.apolloState.ROOT_QUERY")

        # Find employer name
        employer_name_location = driver.find_element_by_xpath('//span[@id="DivisionsDropdownComponent"]')
        employer_name = employer_name_location.get_attribute("innerHTML")
        return fetched_dict, employer_name.lstrip()

    def dict_to_string(self):
        """We will attempt to convert this Python dictionary into a string
        This will be done by using json.dumps to force Python to write the dictionary
        to a file as a string. Then we will read that file, which will return as a string"""

        # Force the dictionary to be written to a file txt
        with open("francis_glassdoor_reviews_scrape_temp.txt", 'w') as file:
            file.write(json.dumps(self.raw_dict_data))

        # Read from the file text
        file = open("francis_glassdoor_reviews_scrape_temp.txt", 'r')
        # using Splitlines is merely best practices
        # This is needed because we will delete file
        return_value = file.read().splitlines()[0]

        # Close file then delete file using os module
        file.close()
        os.remove("francis_glassdoor_reviews_scrape_temp.txt")

        return return_value

    def extract(self):
        """The function that will extract. We will:
        1. Find the index, which is roll, where data should start being extracted.
        """

        # The data should start being extracted from the first open curly bracket {
        # The distance between <"> and the first open curly bracket is 11, hence roll is set as self.the_index + 11
        # self.the_index is put in __init__ as best practices so that it can be referred to if need be
        # Hence the need for roll here.
        roll = self.the_index + 11

        dynamic_count = 0  # This count variable acts as a a flag.

        # There is no post-conditional REPEAT UNTIL loop in python.
        # I do not want the the_end condition to be checked in the first row of loop.
        first_count = True

        the_end = False  # The End will be flipped to True to signify the loop must stop

        # While the end has not been reached, we constantly check every letter starting from the index of roll.
        # If a letter is { then we will add one to the dynamic count flag.
        # If a letter is { then we will subtract 1 from it
        # Repeat this until the dynamic count is balanced (0) which signifies the end point of the interested string.
        # We do exclude the first count
        # The purpose of doing this is that there could be smaller sets or dictionaries inside this rating dictionary,
        # that could begin with { and end with }.
        while not the_end:
            if self.raw_string_data[roll] == '{':
                dynamic_count += 1
                first_count = False
            elif self.raw_string_data[roll] == '}':
                dynamic_count -= 1
            if dynamic_count == 0 and not first_count:
                the_end = True
            roll += 1

        # Return the extracted data from the string
        # We use +12 and -1 here in extracting data to exclude the open curly bracket {
        # and close bracket } of the dictionary
        return self.raw_string_data[(self.the_index + 12):roll - 1]

    def make_dict(self):
        # Declare a temporary dictionary
        # We will also append the company name
        dictionary = {"employerName": self.name}

        # Split EACH property and their values, separated from
        # each other by the comma and a space <, >
        # into elements of keys_and_values
        keys_and_values = self.extracted_string.split(", ")
        time.sleep(2)

        # Loop through each string of keys_and_values
        for index in range(len(keys_and_values)):
            if keys_and_values[index].endswith("}"):  # If an element ends with } we know it is a nested dictionary
                further_split = keys_and_values[index].split(': ', 1)  # Split the string into the key and the value
                # do it only once though to not split the dictionary inside, later versions I will try to convert this
                # into a proper dictionary

                dictionary[further_split[0][1:-1]] = further_split[1]  # put into dictionary the key and value
                # 1:-1 is to exclude the quotes ""
            else:  # If an element does not end with }
                further_split = keys_and_values[index].split(': ')   # Split the string into the key and the value
                try:  # The value is either a float or a string, try convert the value to a float
                    dictionary[further_split[0][1:-1]] = float(further_split[1])
                except ValueError:  # If it results in a ValueError because a string is not convertible to float
                    dictionary[further_split[0][1:-1]] = further_split[1]

        return dictionary

    def __str__(self):  # Just a method to print the dictionary nicely.
        print(self.name)
        for temp_key, temp_value in self.data.items():
            print("{}: {}".format(temp_key, temp_value))
        return "\n"


"""
def scrape_from_google_search(scrape_list):
    #This function accepts a list of employer name
    #Search google, do the scraping
    #then return a list of results of the scraping

    value = []  # list of dictionaries to return

    for entity in scrape_list:
        scrape_url = "https://www.google.com/search?q=glassdoor%20{}%20reviews".format(entity.replace(' ', '%20'))
        driver.get(scrape_url)
        results = driver.find_elements_by_xpath("//div[@class='g']//div[@class='r']//a[not(@class)]")
        for result in results:
            print(result.get_attribute("href"))
        the_link = results.get_attribute("href")
        scrape_entity = WebScrape(the_link)
        print(scrape_entity)
        value.append(scrape_entity.data)

    return value
"""


# TEST USING GOOGLE SEARCH

"""
names = ['accenture', 'new zealand ministry of health', 'beca', 'trimble', 'pwc', 'university of canterbury']
fetched_results = scrape_from_google_search(names)
"""


# TEST USING LINKS

accenture = WebScrape("https://www.glassdoor.co.nz/Reviews/Accenture-Reviews-E4138.htm")
print(accenture)

trimble = WebScrape("https://www.glassdoor.co.nz/Reviews/Trimble-Reviews-E2067.htm")
print(trimble)

beca = WebScrape("https://www.glassdoor.co.nz/Reviews/Beca-Reviews-E114984.htm")
print(beca)

pwc = WebScrape("https://www.glassdoor.co.nz/Reviews/PwC-Reviews-E8450.htm?countryRedirect=true")
print(pwc)

uc = WebScrape("https://www.glassdoor.co.nz/Reviews/University-of-Canterbury-Reviews-E147950.htm")
print(uc)

xero = WebScrape("https://www.glassdoor.co.nz/Reviews/Xero-Reviews-E318448.htm")
print(xero)

ministry_of_health = WebScrape("https://www.glassdoor.co.nz/Reviews/New-Zealand-Ministry-of-Health-Reviews-E137482.htm")
print(ministry_of_health)

