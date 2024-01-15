from selenium.webdriver import Chrome,ChromeOptions
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import re

def scrape_and_write_to_csv():
    driver = Chrome()
    driver.get("http://www.eventkeeper.com/mars/xpages/B/BETHEL/EK.cfm?zeeOrg=BETHEL")
    sleep(5)
    driver.refresh()
    wait = WebDriverWait(driver, 20) 
    all_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='event_date_row']")))
    print(all_dates)
    wait = WebDriverWait(driver, 20)  
    all_events = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='one_event']")))
    with open('event_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['eventTitle','eventAgeGroup', 'eventRegisterLink', 'eventOrganizer','eventOrganizerPhone', 'start_time', 'end_time', 'eventOrganizerEmail', 'eventImageURL', 'eventDescription', 'eventVenueName'])

        for event in all_events:
            eventAge = event.find_element("xpath",".//span/strong")
            eventAgeGroup = eventAge.text
            # keyword_pattern = re.compile(r'(\b(?:grade|ages|kids|years)\b)', re.IGNORECASE)
            # matches = keyword_pattern.findall(eventAgeGroups)
            # if matches:
            #     eventAgeGroup = eventAgeGroups
            # else:
            #     eventAgeGroup = None
            eventTitle = event.find_element("xpath",".//div[@class='event_name']").text

            wait = WebDriverWait(driver, 10)
            input_element = wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='event_registration']/input")))
            eventRegister = input_element.get_attribute("onclick")
            link_start = eventRegister.find("'") + 1
            link_end = eventRegister.rfind("'")
            eventRegisterLink = eventRegister[link_start:link_end]

            time_element = event.find_element("xpath",".//div[@class='event_time']")
            time = time_element.text
            start_time, end_time = map(str.strip, time.split('-'))

            contact_element = event.find_element("xpath", ".//div[@class='event_contact']")
            contact_text = contact_element.text
            contact_info = contact_text.split(':')
            eventOrganizer = contact_info[1].split('(')[0].strip()

            eventOrganizerPhone = ''.join(char for char in contact_info[1].split('(')[1] if char.isdigit())

            eventOrganizerEmail = event.find_element("xpath",".//div[@class='event_contact']/a")

            image_element = event.find_element("xpath", ".//div[@class='event_description']/p[1]/img")
            eventImageURL = image_element.get_attribute("src")

            description = event.find_elements("xpath",".//div[@class='event_description']/p/span")
            eventDescription = description[0].text if description else None  

            location = event.find_element("xpath",".//div[@class='event_location']")
            eventVenueName = location.text if location else None

            print({'eventTitle': eventTitle,
                   'eventDescription':eventDescription,
                   'eventCategory' :None,
                   'eventImageURL' :eventImageURL,
                   'eventCostFree': None,
                   'eventCostLowest': None,
                   'eventCostHighest': None,
                   'eventStartDateTime': start_time,
                   'eventEndDateTime': end_time,
                   'eventPurchaseLink': None,
                   'eventRsvpLink': None,
                   'eventRegisterLink': eventRegisterLink,
                   'eventOrganizer': eventOrganizer,
                   'eventOrganizerEmail': eventOrganizerEmail,
                   'eventOrganizerPhone': eventOrganizerPhone,
                   'eventUrl ': None,
                   'eventAgeGroup': eventAgeGroup,
                   'eventSourceCategories': None,
                   'eventVenueName': eventVenueName,
                   'eventVenueAddress1':None,
                   'eventVenueAddress2':None,
                   'eventVenueTown':'',
                   'eventVenueState': '',
                   'eventVenueZip': '',
                   'eventVenuePhone' : '',
                   'eventVenueEmail': '',
                   'eventVenueURL':'',
                   'eventVenueRoom':'',
                   'eventSourceWebsite': 'http://www.eventkeeper.com/mars/xpages/B/BETHEL/EK.cfm?zeeOrg=BETHEL'
                     })

            csvwriter.writerow([eventTitle, eventAgeGroup, eventRegisterLink, end_time, start_time, eventOrganizerEmail, eventOrganizer, eventOrganizerPhone, eventImageURL, eventDescription, eventVenueName])
    driver.quit()


while True:
    scrape_and_write_to_csv()
    sleep(600)

    
    # all_dates_sets = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='event_date_row']")))
            
    # for date in all_dates_sets:
    #     date_name = date.get_attribute("name")
    #     events_for_date = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//a[@name='{date_name}']/parent::div/following::div[@class='one_event']")))
    #     for event in events_for_date:
    #         eventAge = event.find_element(By.XPATH, ".//span/strong")
    #         eventAgeGroup = eventAge.text
    #         eventTitle = event.find_element(By.XPATH, ".//div[@class='event_name']").text
            

