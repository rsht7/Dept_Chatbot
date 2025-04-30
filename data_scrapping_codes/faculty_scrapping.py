import requests
from bs4 import BeautifulSoup
import json
import time

faculty_urls = [
        
        # URLs here
    ]


faculty_data = []

start_time = time.time()  # Start timer
total_faculty = len(faculty_urls)  #  total count

for idx, url in enumerate(faculty_urls, start=1):  #  enumerate gives index + url
    faculty_name = url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ').title()
    print(f"Scraping ({idx}/{total_faculty}): {faculty_name}...")  #  fancy progress print

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Faculty basic info
    info_table = soup.find('table', class_='table-user-information')
    faculty_info = {}

    if info_table:
        rows = info_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                faculty_info[key] = value

    faculty_info['Name'] = faculty_name

    # Now extract tabbed sections
    tabs = {
        'Publications': 'tabPublications',
        'Projects': 'tabProjects',
        'Memberships': 'tabMemberships',
        'Books Published': 'tabBooks'
    }

    for section_name, tab_id in tabs.items():
        section_items = []
        tab_div = soup.find('div', id=tab_id)
        if tab_div:
            table = tab_div.find('table', class_='views-view-table')
            if table:
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        item_text = cols[1].get_text(strip=True)
                        section_items.append(item_text)
        faculty_info[section_name] = section_items

    faculty_data.append(faculty_info)

# Save everything to a JSON file
with open('faculty_data_all_tabs.json', 'w', encoding='utf-8') as f:
    json.dump(faculty_data, f, indent=4, ensure_ascii=False)

end_time = time.time()  # End timer

elapsed_time = end_time - start_time
print("\nScraping completed and saved to faculty_data_all_tabs.json ✅")
print(f"Total Time Taken: {elapsed_time:.2f} seconds 🕒")
