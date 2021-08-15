from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

driver = webdriver.Chrome("/home/francis/Downloads/chromedriver")


class WebScrape(object):
    """A class to scrape manually"""

    def __init__(self, link):
        self.link = link
        self.name = self.link[36:]
        self.raw_dict_data = self.fetch()
        self.raw_string_data = self.dict_to_string()[0]
        self.the_index = self.raw_string_data.find("\"ratings\": {")
        self.extracted_string = self.extract()
        self.data = self.dictum()

    def fetch(self):
        driver.get(self.link)
        time.sleep(3)
        fetched_dict = driver.execute_script("return appCache.apolloState.ROOT_QUERY")
        time.sleep(2)
        return fetched_dict

    def dict_to_string(self):
        with open('data.txt', 'w') as file:
            file.write(json.dumps(self.raw_dict_data))
        file = open("data.txt", 'r')
        return file.read().splitlines()

    def extract(self):
        roll = self.the_index + 12
        dynamic_count = 0
        first_count = True
        the_end = False
        while not the_end:
            if self.raw_string_data[roll] == '{':
                dynamic_count += 1
                first_count = False
            elif self.raw_string_data[roll] == '}':
                dynamic_count -= 1
            if dynamic_count == 0 and not first_count:
                the_end = True
            roll += 1
        return self.raw_string_data[(self.the_index + 12):roll]

    def dictum(self):
        dictionary = {}
        temp_extracted_list = self.extracted_string

        the_list = self.extracted_string.split(", ")
        print(the_list)
        for index in range(len(the_list)):
            if index + 1 < len(the_list):
                further_split = the_list[index].split(': ')
                dictionary[further_split[0]] = further_split[1]
            else:
                # THIS PART REMAINS PROBLEMATIC
                # RELIES ON THE ASSUMPTION THAT THE FINAL
                # PROPERTY WOULD BE ratedCeo
                dictionary['"ratedCeo"'] = self.extracted_string[-23:]

        return dictionary

    def __str__(self):
        print("Statistics for {}".format(self.name))
        for temp_key, temp_value in self.data.items():
            print("{}: {}".format(temp_key, temp_value))
        return "----"


# TEST

accenture = WebScrape("https://www.glassdoor.co.nz/Reviews/Accenture-Reviews-E4138.htm")
print(accenture)

trimble = WebScrape("https://www.glassdoor.co.nz/Reviews/Trimble-Reviews-E2067.htm")
print(trimble)

beca = WebScrape("https://www.glassdoor.co.nz/Reviews/Beca-Reviews-E114984.htm")
print(beca)

pwc = WebScrape("https://www.glassdoor.co.nz/Reviews/PwC-Reviews-E8450.htm?countryRedirect=true")
print(pwc)