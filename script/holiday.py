#!/usr/bin/env python3
import requests
from icalendar import Calendar
import json, os

class GenerateHolidayAPI:
    def __init__(
        self, 
        url                         = "https://calendar.google.com/calendar/ical/ja.japanese%23holiday%40group.v.calendar.google.com/public/basic.ics"
    ):
        r                           = requests.get(url).text
        self.cal                    = Calendar.from_ical(r)
        self.holidays               = {}
    

    def get(self):
        return self.holidays
    
    def generate(self):
        for component in self.cal.walk():
            if component.name       == "VEVENT":
                date                = component.get('dtstart').dt.isoformat()
                summary             = str(component.get('summary'))
                self.holidays[date] = summary
    
    def dump(
        self,
        folder          = "docs/holiday"
    ):
        os.makedirs(folder, exist_ok=True)
        with open(f"{folder}/holiday.json", "w", encoding="UTF-8") as f:
            json.dump(self.holidays, f, ensure_ascii=False, indent=4, sort_keys=True)

    def sort_key(self):
        self.holidays = dict(sorted(self.holidays.items()))
    
    def dump_each_year(
        self,
        folder          = "docs/holiday"
    ):
        os.makedirs(folder, exist_ok=True)
        self.sort_key()
        keys    = list(self.holidays.keys())
        
        if not keys:
            return 
        
        first   = int(keys[0].split("-")[0])        # yyyy-mm-dd
        last    = int(keys[-1].split("-")[0])
        for y in range(first+1, last):
            filtered = {
                k: v for k, v in self.holidays.items() if k.startswith(f"{y}-")
            }

            with open(f"{folder}/{y}.json", "w", encoding="UTF-8") as f:
                json.dump(filtered, f, ensure_ascii=False, indent=4, sort_keys=True)


if __name__=="__main__":
    api = GenerateHolidayAPI()
    api.generate()
    api.dump()
    api.dump_each_year()