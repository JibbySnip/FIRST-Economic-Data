import re
import requests
import matplotlib
from collections import defaultdict
from message_utils import send_message_to_single_recipient
from os import get_env


attribution = "This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau."

cached_loc_coords = defaultdict(None)


def get_teams():
    """Returns a list of team models"""
    params = {
        "country": "usa",
        "Content-Type": "application/json",
        "X-TOA-Key": str(get_env("TOA_KEY")),
        "X-Application-Origin": "FIRST Economic Graph",
    }


def get_fips(lat, lon):
    """Returns the FIPS Code of the coordinates"""
    fips_params = {"latitude": lat, "longitude": lon, "format": "json"}
    fips_res = requests.get("https://geo.fcc.gov/api/census/block/find", fips_params)
    if fips_res.status_code == 200:
        return fips_res.json()["County"]["FIPS"]
    else:
        return None


def get_coords(loc):
    """Returns the coordinates of the county"""
    if cached_loc_coords["loc"] != None:
        return cached_loc_coords["loc"]
    coords_params = {"q": loc, "key": str(get_env("COORD_KEY"))}
    coords_res = requests.get("https://api.opencagedata.com/geocode/v1/json")
    if coords_res.status_code == 200:
        geometry = coords_res.json()["results"]["geometry"]
        cached_loc_coords[loc] = (geometry["lat"], geometry["long"])
        return geometry["lat"], geometry["long"]
    elif coords_res.status_code == 402:
        return 402
    else:
        return None


if __name__ == "__main__":
    pass
