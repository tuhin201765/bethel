from selenium.webdriver import Chrome,ChromeOptions
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os


driver = Chrome()
driver.get("http://www.eventkeeper.com/mars/xpages/B/BETHEL/EK.cfm?zeeOrg=BETHEL")
sleep(5)
driver.refresh()
wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
all_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='event_date_row']")))
print(len(all_dates))
wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
all_events = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='one_event']")))
for event in all_events:
    name = event.find_element("xpath","//div[@class='event_name']").text
    date_element = event.find_element("xpath","//div[@class='event_time']")
    date = date_element.text
    mail = event.find_element("xpath","//div[@class='event_contact']/a").accessible_name
    # image_url = event.find_element("xpath","//div[@class='event_description']/p[1]/img/@src")
    description = event.find_elements("xpath","//div[@class='event_description']/p/span")
    if description:
        description = description[0].text
    # contact = event.find_element("xpath","//div[@class='event_contact']/text()[1]")
    location = event.find_element("xpath","//div[@class='event_location']")
    if location:
        location = location.text
    else:
        pass


    print(name)
print(len(name)) 
print(len(all_events))

