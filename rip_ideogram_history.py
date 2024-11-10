import cloudscraper
import json
import time
import os

ideogram_base_url = "https://ideogram.ai/api/g/u"

howto_use = """
1. You have to fill in a couple of values below to make this work
2. You have to have python3 installed and you will run this like python rip_ideogram_history.py or python3 rip_ideogram_history.py
3. You probably have to do things like 'pip install cloudscraper' or 'pip3 install cloudscraper' in your python environment to get that library installed.
4. But before that you have to fill in some private values related to your authentication on ideogram, within this very file itself.
5. I'm not going to copy or take advantage of your info, but in general, be very careful with the development tools tab. The data you are reading and entering is enough to authenticate as you, so don't share it if people ask for it.
6. For safety, whenever anyone asks for that, please think about maybe posting the whole script or situation to an LLM for analysis, like claude/chatgpt, asking if this is safe to run or if it will leak your data.  
7. That includes this case - please check this script out and validate it's safe by posting into ChatGPT and asking something like "is there anything in this script which would copy/steal/or incorrectly use my tokens/authentication details here?"

That out of the way, here is what you have to get:

1. Your "bearer" authentication token from being logged in to ideogram.
2. Your cookies from the browser, in a development tools window, opened from a logged-in ideogram page you are on.

How to do this

1. Visit ideogram.ai, say in chrome or firefox (my choice)
2. Hit F12 to pop up 'development tools'.
3. Don't get intimidated - you are all right. Step by step.
4. Go to the "Network" tab.
5. Now click back to the browser window and scroll down say on your profile view, or any other page so that your browser will send a request to ideogram
6. then in dev tools, a new row will appear in the list of requests to ideogram.ai
7. If you click on it you can see details on the right, like Headers, Cookies, etc.
8. On the right side within that, there is a tab for the "request headers" section and Authorization part.
9. Copy the entire value of the Authorization header which starts "Bearer" and put that below into YOUR_BEARER
10. Copy the entire value of the Cookie header. (right-click and do "copy value" or similar.  Put that into this script below where it says YOUR_COOKIE
11. Also update your username like below, by replacing YOUR_USERNAME with your actual username
12. Then you can run this script. It'll create a subfolder which will have the json files for all your public/private history of requests to ideogram.
"""

# ------------------------- ONLY MODIFY THE SCRIPT HERE IN THIS AREA.----------------------------------

#this will start out like "Bearer ... long string of random chars"
YOUR_BEARER="REPLACE_THIS"

# This will probably start out like "AMP_da0464495c=... very long"
YOUR_COOKIE="REPLACE_THIS"

# The string of your username on ideogram
YOUR_USERNAME="REPLACE_THIS"

# Yes, we do repeat things like YOUR_BEARER below, but those will be automatically filled in after you enter them in this section.
# You *only* need to modify this section, no other sections or changes required besides adding these 3 values.




# ------------------------- END OF USER MODIFIABLE AREA OF THE SCRIPT ----------------------------------

def parse_cookies(cookie_string):
    return {name: value for name, value in (cookie.split('=', 1) for cookie in cookie_string.split('; ') if '=' in cookie)}

# NOTE: do NOT replace the values here. 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": f"https://ideogram.ai/u/{YOUR_USERNAME}/generated",
    "Content-Type": "application/json",
    "Authorization": YOUR_BEARER,
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4",
    "TE": "trailers",
}

required_cookies = [
    "__cf_bm",
    "AMP_da0464495c",
    "AMP_MKTG_da0464495c",
    "cf_clearance",
    "ph_phc_yQgAEdJJkVpI24NdSRID2mor1x1leRpDoC9yZ9mfXal_posthog",
    "session_cookie"
]



scraper = cloudscraper.create_scraper()
save_folder_name="ideogram_requests"
os.makedirs(save_folder_name, exist_ok=True)

all_data = []

cookies = parse_cookies(YOUR_COOKIE)

def fetch_page(page, doPrivate):
    params = {
        "user_id": YOUR_USERNAME,
        "filters": ["generations", "upload", "edit", "upscales"],
    }
    if page>0:
        params["page"] = page
    if doPrivate:
        params['private']="true"
    
    response = scraper.get(ideogram_base_url, headers=headers, params=params, cookies=cookies)
    
    print(f"Fetching URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")
    #print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error Response Content: {response.text}")
        return None

print("getting all non-private first, then private generation histories.  Warning: as you do more generations, ideogram basically re-paginates your archive of requests. So, the items that exist in page 3 on one day may shift to page 6 later. So if you run this multiple times, you'll have to figure out a system for deduplication & avoiding overwriting.")

for val in [False, True]:
    page = 0
    while True:
        print(f"\nFetching page {page}... private={val}")
        
        data = fetch_page(page, val)
        
        if data is not None:
            if isinstance(data, list):
                page_items = data
            else:
                page_items = data.get("items", [])
            
            all_data.extend(page_items)
            
            # Save individual page data
            privateText=""
            if val:
                privateText="-private"
            target = f"{save_folder_name}/page_{page}{privateText}.json"
            with open(target, "w") as f:
                json.dump(page_items, f, indent=2)
            
            print(f"Page {page} fetched and saved to {target}. Items: {len(page_items)}")
            
            if isinstance(data, dict) and not data.get("has_more", False):
                print("No more pages to fetch.")
                break
            elif isinstance(data, list) and len(page_items) == 0:
                print("No more items to fetch.")
                break
            
            page += 1
            # Add a delay to avoid rate limiting
            time.sleep(19)  
        else:
            print(f"Error fetching page {page}. Stopping.")
            break

# Save all data to a JSON file
with open("ideogram_data_all.json", "w") as f:
    json.dump(all_data, f, indent=2)

print(f"\nTotal items collected: {len(all_data)}")
print("All data saved to ideogram_data_all.json")
print(f"Individual page data saved in the '{save_folder_name}' directory")
