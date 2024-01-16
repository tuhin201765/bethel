import requests
from lxml import html
import re
# import schedule
from datetime import datetime
from subprocess import run
import pandas as pd

def extract_event_info(root,start_date,end_date):
    if end_date != None:
        xpath = f"""//div[@class='one_event' 
                    and 
                    preceding-sibling::div[@class='event_date_row']/a[@name='{start_date}'] 
                    and 
                    following-sibling::div[@class='event_date_row']/a[@name='{end_date}'] ]"""
    else:
        xpath = f"""//div[@class='one_event' 
                    and 
                    preceding-sibling::div[@class='event_date_row']/a[@name='{start_date}']]"""
        
    events = root.xpath(xpath)

    for event in events:
        event_dict = dict()
        eventTitle = event.xpath(".//div[@class='event_name']/text()")
        if eventTitle:
            event_dict['eventTitle'] = eventTitle[0].strip()
        else:
            event_dict['eventTitle'] = None
        time_element = event.xpath(".//div[@class='event_time']/text()[1]")
        for item in time_element:
            if isinstance(item, str):
                start_time, end_time = item.split('-')
                start_time = start_time.strip()
                end_time = end_time.strip()
                start_time_dt = datetime.strptime(start_time, '%I:%M %p')
                end_time_dt = datetime.strptime(end_time, '%I:%M %p')

                # Format start_time and end_time as "00:00:00"
                formatted_start_time = start_time_dt.strftime('%H:%M:%S')
                formatted_end_time = end_time_dt.strftime('%H:%M:%S')

        description = event.xpath(".//div[@class='event_description']//p/span//text()")
        eventDescription = ' '.join(description).strip()


        eventAgeGroup_elements = event.xpath(".//span/strong/text()")
        keywords = ['kids', 'children', 'ages', 'grades','years','old','grade']
        filtered_eventAge = [text for text in eventAgeGroup_elements if any(keyword in text.lower() for keyword in keywords)]
        filtered_eventAgeGroup = filtered_eventAge[0] if filtered_eventAge else None

        eventRegister = event.xpath(".//div[@class='event_registration']/input/@onclick") 
        eventRegisterLink = eventRegister[0].split("'")[1] if eventRegister else None
        
        contact_element = event.xpath(".//div[@class='event_contact']/text()")
        contact_info_list = [str(element).strip() for element in contact_element]

        if contact_info_list:
            eventOrganizer = contact_info_list[0].replace("CONTACT:", "").strip().split('(')[0].strip().split('\xa0')[0]
            event_dict['eventOrganizer'] = eventOrganizer
        else:
            event_dict['eventOrganizer'] = None

        eventOrganizerPhone = re.sub(r'\D', '', contact_info_list[0]) if contact_info_list else None
        
        eventOrganizerEmail_element = event.xpath(".//div[@class='event_contact']/a/@href")
        eventOrganizerEmail = eventOrganizerEmail_element[0].split(':')[-1] if eventOrganizerEmail_element else None

        image_url = event.xpath(".//div[@class='event_description']/p[1]/img/@src")
        eventImageURL = image_url[0] if image_url else None
        
        location_element = event.xpath(".//div[@class='event_location']/text()")
        eventVenueName = location_element[0].replace('LOCATION:', '').strip() if location_element else None

        event_dict['eventDescription'] = eventDescription
        event_dict['eventOrganizerEmail'] = eventOrganizerEmail
        event_dict['eventAgeGroup'] = filtered_eventAgeGroup
        event_dict['eventRegisterLink'] = eventRegisterLink
        event_dict['eventOrganizerPhone'] = eventOrganizerPhone
        event_dict['eventImageURL'] = eventImageURL
        event_dict['eventVenueName'] = None
        event_dict['eventStartDateTime'] = f"{start_date} {formatted_start_time.strip()}"
        event_dict['eventEndDateTime'] = f"{end_date} {formatted_end_time.strip()}"
        event_dict['eventCategory'] = None
        event_dict['eventCostFree'] = 'Y'
        event_dict['eventCostLowest'] = None
        event_dict['eventCostHighest'] = None
        event_dict['eventRsvpLink'] = None
        event_dict['eventUrl '] = None
        event_dict['eventSourceCategories'] = None
        event_dict['eventSourceWebsite  '] = 'http://www.eventkeeper.com/'
        event_dict['eventVenueAddress1'] = '189 Greenwood Avenue. Bethel, CT 06801.'
        event_dict['eventVenueAddress2'] = None
        event_dict['eventVenueTown'] = ' Bethel'
        event_dict['eventVenueState'] = 'CT'
        event_dict['eventCostHighest'] = None
        event_dict['eventVenueZip'] = '06801'
        event_dict['eventVenuePhone'] = '2037948756'
        event_dict['eventVenueEmail'] = None
        event_dict['eventVenueURL'] = None
        event_dict['eventVenueRoom'] = eventVenueName
        event_dict['eventPurchaseLink'] = None

        print(event_dict)




# Print the values
def scrape_eventkeeper():
    testing = True
    if not testing:
        url = 'http://www.eventkeeper.com/mars/xpages/B/BETHEL/EK.cfm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

        response = requests.get(url, headers=headers)
        # Assuming you have the HTML content in the 'response' variable
        html_content = response.text
    else:
        with open('html_content.txt', 'r', encoding='utf-8') as file:
            html_content = file.read()

    root = html.fromstring(html_content)

    dates = root.xpath('//div[@class="event_date_row"]/a/@name')
    all_events_data = []
    for i in range(len(dates)):
        start_date = dates[i]
        if i != len(dates)-1:
            end_date = dates[i+1]
        else:
            end_date = None
        
        events_data = extract_event_info(root=root,start_date=start_date,end_date=end_date)
        for ed in events_data:
            all_events_data.append(ed)
    
        return all_events_data

if __name__=='__main__':
    data = scrape_eventkeeper()

    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
# if __name__ == '__main__':
#     # Schedule the script to run every 10 minutes
#     schedule.every(10).minutes.do(scrape_eventkeeper)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)