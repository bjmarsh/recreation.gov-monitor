import os,sys
import datetime as dt
import requests
import json
from ses import send_email

def get_by_date(camp_id, date):
    headers = {
        'pragma': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,da;q=0.8,mt;q=0.7',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'sec-fetch-mode': 'cors',
        'accept': 'application/json, text/plain, */*',
        'cache-control': 'no-cache, no-store, must-revalidate',
        'authority': 'www.recreation.gov',
        'referer': 'https://www.recreation.gov/camping/campgrounds/234015/availability',
        'sec-fetch-site': 'same-origin'
        }

    url = 'https://www.recreation.gov/api/camps/availability/campground/{0}/month?start_date={1}-{2:02d}-01T00%3A00%3A00.000Z'.format(camp_id, date.year, date.month)

    r = requests.get(url, headers=headers)
    
    # print r.status_code
    # print r.text

    if r.status_code != 200:
        print(r.text)
        raise Exception("ERROR! status code {0}. See text above.".format(r.status_code))

    data = json.loads(r.text)

    sites = {}
    for site_id, sdata in data["campsites"].items():
        sname = sdata["loop"].split()[-1]+sdata["site"]
        sites[sname] = {}
        sites[sname]["type"] = sdata["campsite_type"]
        sites[sname]["availability"] = sdata["availabilities"]["{0}-{1:02d}-{2:02d}T00:00:00Z".format(date.year,date.month,date.day)]

    return sites

year, month, day = tuple(int(x) for x in sys.argv[1:])
date = dt.date(year,month,day)
camp_ids = {
    # 231880: "Difficult Campground",
    231881: "Silver Bar",
    231882: "Silver Bell",
    231883: "Silver Queen",
    }
avail = []
for camp_id, name in camp_ids.items():
    print("Getting availability for {0} ({1}) on date {2}".format(name, camp_id, date))
    sites = get_by_date(camp_id, date)
    for site,info in sites.items():
        if info["availability"] == "Available" and info["type"] != "RV ELECTRIC":
            avail.append((camp_id, name,  site, info["type"]))

s = "The following campsites are available on {0}:\n".format(date)
for av in avail:
    s += "{1} ({0}): Site {2} ({3})\n".format(*av)

for camp_id in camp_ids:
    s += "\nhttps://www.recreation.gov/camping/campgrounds/{0}/availability\n".format(camp_id)

print(s)
if len(avail) > 0:
    # os.system("printf \"{0}\" | mail -s 'Campgrounds available {1}' {2}".format(s.replace('\n','\\n'), date, email))
    send_email("Campgrounds available {0}".format(date), s)
