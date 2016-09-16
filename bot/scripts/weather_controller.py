import sys
import os
import time
import optparse
import json
import logging
import urllib2
import time
from . import weather_manager

logger = logging.getLogger(__name__)
from xml.etree.ElementTree import XML
from datetime import datetime, timedelta

API="954b5bfc706747b6aff23600161607"
URL="http://api.worldweatheronline.com/premium/v1/weather.ashx"

CITY="Winnipeg"
SUNSET_HOUR = 21
SUNRISE_HOUR = 5
HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg

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
        if "sunny" in conds:
            return ":sunny:"
        if "clear" in conds:
            curr_datetime = datetime.utcnow() - timedelta(hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS) #change here when daylight savings ends
            curr_time = int(curr_datetime.strftime('%H'))
            if curr_time >= SUNSET_HOUR or curr_time < SUNRISE_HOUR:
                return ":night_with_stars:"
            else:
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
            response = urllib2.urlopen(URL+"?key="+API+"&q="+CITY+"&num_of_days=1")
        # except urllib2.URLError as e: # works but is not needed
        except Exception as e:
            my_string = weather_manager.getCurrentWeather()
            # my_string = (":zacefron: Have a very merry time "
            #              "not knowing the weather :theotherzacefron:")
            response = str(e) + "\n" + my_string
            return response
        else:
            data = response.read().decode('utf-8')
            temp = XML(data).find("current_condition").find("temp_C").text
            feels_like = XML(data).find("current_condition").find("FeelsLikeC").text
            conditions = XML(data).find("current_condition").find("weatherDesc").text
            icon = WeatherController.get_icon(str.lower(conditions))
            if int(feels_like) != int(temp):
                return "Winnipeg is currently :zacefron: "+temp+"C but feels like :theotherzacefron: "+feels_like+"C and conditions are "+conditions+" "+icon
            else:
                return "Winnipeg is currently :zacefron: "+temp+"C and conditions are "+conditions+" "+icon
    get_weather = staticmethod(get_weather)
