import json
import re
import requests
import urllib.request
import os
import time
import numpy as np
import spacy
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from ratelimit import limits, sleep_and_retry
from IPython.display import clear_output
from credentials import * # These are the credentials
import re

final_json = {}
try:
    with open('proof_of_concept/data.json', 'r') as file:
        final_json = json.load(file)
except json.JSONDecodeError as e:
    raise Exception(f'Error: {e}')

# Obtain the artists
TOP_ARTISTS = list(final_json.keys())


# 1 call per second
CALLS = 1
RATE_LIMIT = 1

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    # Empty function to limit calls to APIs
    return


artists = {}
photos = {}

# This function will be used later. It calls the Seatgeek API to add alternative prices to an event, and enrich our original data
# To find the event, we make a call using the artist name and the date
def find_alternative_price(artist, date, time):
    # We need to transform data in order to have the Seatgeek API understand it
    search_artist = artist.replace(" ", "-")
    search_date = date + "T" + time
    # We need to have the search terms be in ASCII code for the Seatgeek API to work
    if len(search_artist) != len(search_artist.encode()):
        return "Inexistent"

    search = f"https://api.seatgeek.com/2/events?performers.slug={search_artist}&datetime_local={search_date}&client_id={SEATGEEK_API_CLIENT_ID}"
    check_limit()
    with urllib.request.urlopen(search) as url:  
        data = json.loads(url.read().decode())

    # We make sure that there is only one concert as result (more would mean we cannot find the exact concert, less would mean that the concert is not on Seatgeek)
    # Then, we take the lowest price for that event and return it
    if data["meta"]["total"] == 1:
        return data["events"][0]["stats"]["lowest_price"]

    # If something fails along the way, we return that there is no alternative price
    return "Inexistent"

# We will find the unique Ticketmaster API identifier of each artist using their name. We will store it in a dictionary 
# We need to do this in order to find only the concerts of the original artist (not tribute concerts for example)
for keyword in TOP_ARTISTS:
    # regx = re.compile('\W')
    # if_space = regx.findall(keyword)
    keyword = keyword.replace(" ", "")
    # We make a call to the Tickermaster API and store the information, downloaded in json format, in a dictionary
    search = f"https://app.ticketmaster.com/discovery/v2/attractions.json?&keyword={keyword}&apikey={TICKETMASTER_API_KEY}"
    check_limit() 
    with urllib.request.urlopen(search) as url:  
        data = json.loads(url.read().decode())

    # We access the section of the dictionary in which the id's of artists are stored, and retrieve it
    attractions = data["_embedded"]["attractions"]
    for attraction in attractions:
        if attraction["name"].replace(" ", "") == keyword:
            artists[attraction["name"]] = attraction["id"]
            # Extra information, used only for Part 2
            photos[attraction["name"]] = []
            images = attraction["images"]
            for image in images:
                photos[attraction["name"]].append(image["url"])

# Extra information, used only for Part 2
with open('photos.json', 'w') as file:
        json.dump(photos, file, indent=4)
                

# We will find concert information for all of the concerts of each artist (using their id), and store it in a dictionary
information = {}
for artist in artists:
    # We make a call to the Tickemaster API.
    search = f"https://app.ticketmaster.com/discovery/v2/events.json?&attractionId={artists[artist]}&apikey={TICKETMASTER_API_KEY}"    
    check_limit()
    with urllib.request.urlopen(search) as url:  
        data = json.loads(url.read().decode())
    
    # We discard artists with no upcoming concerts
    if data["page"]["totalElements"] == 0:
        continue

    # We create an entry in the dictionary for each artist. It will have a list of concerts
    information[artist] = []
    events = data["_embedded"]["events"]
    for event in events:
        try:
            # Some fields are absolutely necessary for the functionality of the app: name, url, date and time, price, and venue
            # Thus, if they are not available in the original data source we will ignore that concert
            name = event["name"]
            url = event["url"]

            date = event["dates"]["start"]["localDate"]
            time = event["dates"]["start"]["localTime"]
            timezone = event["dates"]["timezone"]

            # We take the lowest price (remember that we want to find the cheapest, most convenient event).
            # We will ignore concerts with a price of 0€ (since in this context it usually indicates that prices have not been oficially released yet)
            prices = event["priceRanges"]
            minPrice = min(prices, key=lambda x:x['min'])
            cheapestPrice = minPrice["min"]
            currency = minPrice["currency"]
            if cheapestPrice == 0: 
                raise KeyError('nullPrice')
            
            venue = event["_embedded"]["venues"][0]
            venueName = venue["name"]

            # Using the information we have from Ticketmaster, we look for the price of the same concert on Seatgeek
            alternativeCheapestPrice = find_alternative_price(artist, date, time)

            # We have stored the information in variables while checking it is valid. 
            # When the checks have finished, we will store the information in a dictionary for each concert.
            information[artist].append({})
            information[artist][-1]["Concert Name"] = name
            information[artist][-1]["Concert URL"] = url
            information[artist][-1]["Date"] = date
            information[artist][-1]["Time"] = time
            information[artist][-1]["Timezone"] = timezone
            information[artist][-1]["Ticketmaster Cheapest Price"] = cheapestPrice
            information[artist][-1]["Seatgeek Cheapest Price"] = alternativeCheapestPrice
            information[artist][-1]["Currency"] = currency
            information[artist][-1]["Venue"] = venueName

            # Some more information is optional: city, country, classifications (concert genre), parking information, accesibility information
            # We will check if it is available, else we will simply indicate that it is not (but still keep the concert in our list)
            if "city" in venue: 
                information[artist][-1]["City"] = venue["city"]["name"]
            else: 
                information[artist][-1]["City"] = "Not Specified"

            if "country" in venue: 
                information[artist][-1]["Country"] = venue["country"]["name"]
            else:
                information[artist][-1]["Country"] = "Not Specified"

            if "classifications" in event and len(event["classifications"]) > 0 and "genre" in event["classifications"][0]: 
                information[artist][-1]["Main Genre"] = event["classifications"][0]["genre"]["name"]
            else: 
                information[artist][-1]["Main Genre"] = "Not Specified"
            if "products" in event: 
                products = event["products"]
                for product in products:
                    if product == "Parking": 
                        information[artist][-1]["Parking Service"] = "Yes"
                        break
                else: 
                    information[artist][-1]["Parking Service"] = "No"
            if "accessibility" in event and "info" in event["accessibility"]:
                information[artist][-1]["Accessibility Services"] = "Yes"
            else:
                information[artist][-1]["Accessibility Services"] = "No"    

            # Extra Information, used only for part 2
            print(venue)
            print(venue["location"])
            print(venue["location"]["latitude"])
            print(venue["location"]["longitude"])
            latitude = venue["location"]["latitude"]
            longitude = venue["location"]["longitude"]

            information[artist][-1]["Latitude"] = latitude
            information[artist][-1]["Longitude"] = longitude        
        
        except KeyError as e:
            pass

    else:
        # We delete information about an artist if no concerts have been found (or only concerts with incomplete information)
        if information[artist] == []:
            del information[artist]

# We store the information in the final json file
for artist in final_json:
    if 'Concerts' not in final_json[artist]:
        final_json[artist]['Concerts'] = {}

    if artist in information:
        final_json[artist]['Concerts'] = information[artist]