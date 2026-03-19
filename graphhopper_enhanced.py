# ============================================================
# Team Name  : [Team Snowbear V2]
# Members    :
#   1. Christian Louis Suico   - Lead Developer / API Integration
#   2. Jay Talingting          - Feature Developer / Transport Modes [DONE]
#   3. Jan Earl Tampus         - Feature Developer / Estimator Functions
#   4. Wilfred Cholo Penales   - Tester / Documentation
# Project    : Project Activity 3 - Social Coding
# Option     : Option 1 - Feature Enhancements of Lab 4.9.2
# Features Added:
#   1. Additional transport modes: scooter, wheelchair
#   2. Estimated fuel cost (for car/scooter) in liters and PHP
#   3. Estimated calorie burn (for bike, foot, wheelchair)
# How to run : python3 graphhopper_enhanced.py
# Requires   : pip install requests
# ============================================================

import requests
import urllib.parse

key = "YOUR_API_KEY_HERE"
route_url = "https://graphhopper.com/api/1/route?"


def geocoding(location, key):
    while location == "":
        location = input("  Location cannot be empty. Please enter again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata   = requests.get(url)
    json_data   = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat   = json_data["hits"][0]["point"]["lat"]
        lng   = json_data["hits"][0]["point"]["lng"]
        name  = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0]["country"] if "country" in json_data["hits"][0] else ""
        state   = json_data["hits"][0]["state"]   if "state"   in json_data["hits"][0] else ""
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        print("  Geocoding API -> " + new_loc + " (Type: " + value + ")")
        print("  URL: " + url)
    else:
        lat     = "null"
        lng     = "null"
        new_loc = location
        if json_status != 200:
            print("  Geocode API Error [" + str(json_status) + "]: " + json_data["message"])
    return json_status, lat, lng, new_loc


def estimate_fuel(distance_km):
    fuel_efficiency = 12.0
    price_per_liter = 63.0
    liters_used = distance_km / fuel_efficiency
    cost_php    = liters_used * price_per_liter
    print("  Estimated Fuel Used : {:.2f} liters".format(liters_used))
    print("  Estimated Cost      : PHP {:.2f}".format(cost_php))
    print("     (Based on ~{} km/L efficiency at PHP {:.0f}/L)".format(
          int(fuel_efficiency), price_per_liter))


def estimate_calories(distance_km, vehicle):
    speed_kmh = {"bike": 15.0, "foot": 5.0, "wheelchair": 4.0}
    met_value = {"bike": 7.5,  "foot": 3.8, "wheelchair": 3.5}
    body_weight_kg = 65.0
    time_hours     = distance_km / speed_kmh[vehicle]
    calories       = met_value[vehicle] * body_weight_kg * time_hours
    print("  Estimated Calories Burned : {:.0f} kcal".format(calories))
    print("     (Assumes 65 kg body weight, {:.0f} km/h avg speed)".format(speed_kmh[vehicle]))


while True:
    print("\n" + "+" * 50)
    print("  Vehicle profiles available:")
    print("+" * 50)
    print("  car, bike, foot, scooter, wheelchair")
    print("+" * 50)
    valid_profiles = ["car", "bike", "foot", "scooter", "wheelchair"]
    vehicle = input("  Enter a vehicle profile (or q to quit): ").strip().lower()
    if vehicle in ("quit", "q"):
        print("\n  Goodbye! Safe travels.")
        break
    if vehicle not in valid_profiles:
        vehicle = "car"
        print("  Invalid profile entered - defaulting to: car")
    loc1 = input("\n  Starting Location: ").strip()
    if loc1 in ("quit", "q"):
        print("\n  Goodbye! Safe travels.")
        break
    orig = geocoding(loc1, key)
    loc2 = input("\n  Destination: ").strip()
    if loc2 in ("quit", "q"):
        print("\n  Goodbye! Safe travels.")
        break
    dest = geocoding(loc2, key)
    print("\n" + "=" * 50)
    if orig[0] == 200 and dest[0] == 200:
        gh_vehicle = vehicle
        if vehicle == "scooter":
            gh_vehicle = "car"
        elif vehicle == "wheelchair":
            gh_vehicle = "foot"
        op        = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp        = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": gh_vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data   = requests.get(paths_url).json()
        print("  Routing API Status : " + str(paths_status))
        print("  Routing URL        : " + paths_url)
        print("=" * 50)
        print("  Directions from {} to {} by {}".format(orig[3], dest[3], vehicle))
        print("=" * 50)
        if paths_status == 200:
            distance_m = paths_data["paths"][0]["distance"]
            km    = distance_m / 1000
            miles = km / 1.61
            sec   = int(paths_data["paths"][0]["time"] / 1000 % 60)
            mins  = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr    = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("  Distance : {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("  Duration : {0:02d}:{1:02d}:{2:02d}".format(hr, mins, sec))
            print("=" * 50)
            for each in range(len(paths_data["paths"][0]["instructions"])):
                step_text = paths_data["paths"][0]["instructions"][each]["text"]
                step_dist = paths_data["paths"][0]["instructions"][each]["distance"]
                print("  {0} ( {1:.1f} km / {2:.1f} mi )".format(
                      step_text, step_dist / 1000, step_dist / 1000 / 1.61))
            print("=" * 50)
            print("\n  Trip Estimate for '{}'".format(vehicle))
            print("-" * 50)
            if vehicle in ("car", "scooter"):
                estimate_fuel(km)
            else:
                estimate_calories(km, vehicle)
            print("-" * 50)
        else:
            print("  Routing Error: " + paths_data["message"])
            print("*" * 50)
    else:
        print("  Could not resolve one or both locations. Please try again.")
        print("=" * 50)
