import sys
import os
import time
import optparse
import json 
import urllib

from xml.etree.ElementTree import XML

API="43ff7b292dd04d4dacd230358160305"
URL="http://api.worldweatheronline.com/premium/v1/weather.ashx"
 
CITY="Winnipeg"

class WeatherController:

    def get_icon(conds):
        if "tornado" in conds or "hurricane" in conds or "cyclone" in conds:
            return ":cyclone:"
        if "light rain" in conds or "patchy rain" in conds:
            return ":closed_umbrella:"
        if "rain" in conds:
            return ":umbrella:"
        if "thunder" in conds:
            return ":zap:"
        if "snow" in conds:
            return ":snowflake:"
        if "fog" in conds or "mist" in conds:
            return ":foggy:"
        if "cloud" in conds or "overcast" in conds:
            return ":cloud:"
        if "sunny" in conds or "clear" in conds:
            return ":sunny:"
        if "drizzle" in conds or "sleet" in conds:
            return ":umbrella:"
        if "tsunami" in conds:
            return ":ocean:"
        if "fire" in conds:
            return ":fire:"
        if "smog" in conds:
            return ":shit:"
        if "wind" in conds:
            return ":flags:"
        if "eclipse" in conds:
            return ":new_moon_with_face:"
        else:
            return ":zacefron:"
    get_icon = staticmethod(get_icon)

    def get_weather():
        
        try:
             response = urllib.urlopen(URL+"?key="+API+"&q="+CITY+"&num_of_days=1")
             #req = urllib.request.Request(URL+"?key="+API+"&q="+CITY+"&num_of_days=1")
        except urllib.error.URLError as e: 
            return ":zacefron: wishes you a very merry time not knowing the weather :theotherzacefron:"
        else:
            data = response.read().decode('utf-8')
            temp = XML(data).find("current_condition").find("temp_C").text
            feels_like= XML(data).find("current_condition").find("FeelsLikeC").text
            conditions= XML(data).find("current_condition").find("weatherDesc").text
            icon = WeatherController.get_icon(str.lower(conditions))
            return "Winnipeg is currently :zacefron: "+temp+"C but feels like "+icon+" "+feels_like+"C and conditions are "+conditions+" :theotherzacefron:"
    get_weather = staticmethod(get_weather)
