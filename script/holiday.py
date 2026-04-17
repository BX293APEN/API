#!/usr/bin/env python3
import requests
from icalendar import Calendar
import json

class GenerateHolidayAPI:
    def __init__(
        self, 
        url             = "https://calendar.google.com/calendar/ical/ja.japanese%23holiday%40group.v.calendar.google.com/public/basic.ics"
    ):
        r               = requests.get(url).text
        self.cal        = Calendar.from_ical(r)
        self.holidays   = {}
        
    def generate(self):
        for component in self.cal.walk():
          if component.name == "VEVENT":
            date        = component.get('dtstart').dt.isoformat()
            summary     = str(component.get('summary'))
            self.holidays[date] = summary
        
        return self.holidays
    
    def dump(
        self,
        output          = "docs/holiday.json"
    ):
        with open(output, "w", encoding="UTF-8") as f:
            json.dump(self.holidays, f, ensure_ascii=False, indent=4, sort_keys=True)
            

if __name__=="__main__":
    api = GenerateHolidayAPI()
    api.generate()
    api.dump()