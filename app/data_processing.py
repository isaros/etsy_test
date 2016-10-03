
# coding: utf-8

import httplib
import json
import re
from HTMLParser import HTMLParser

import utils

#------ CONSTANTS ------#
# TODO: Use something else than a variable to store the API KEY (flag, env variable...)
API_KEYSTRING = 'r0asz7dc58itf9cq0p7bx34y'
MAX_LISTINGS_LENGTH = 100 # Number max of listing_id allowed to be requested in a single call


#------ UTILS Functions and Class ------#

# Create a class to handle context management with http connection
class HTTPSContextManager():
    def __init__(self, url):
        self._url = url
        self._connection = None

    def __enter__(self):
        self._connection = httplib.HTTPSConnection(self._url)
        return self._connection

    def __exit__(self, cls, value, tb):
        self._connection.close()


# Convert a list of int to a proper url query-string
def listing_to_querry_string(listing):
    return "%2C+".join(map(lambda e : str(e),listing))


## Preprocess and clean title
# NOTE :
# I was not sure about the html entities whether it has to handle html tag as well.
# Given the context I considered that it was not need.
# For now I remove every non-alphanumeric characters not only leading and trailing
# TODO :
#    Remove any leading or trailing non-alphanumeric characters from each token
#    Any tokens containing only non-alphanumeric characters should be ignored
def title_cleaning(string):
    h=HTMLParser()
    string = h.unescape(string)
    string = re.sub(r"[^A-Za-z0-9]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


## Read and fetch the listing from a file with file_name
def read_file(file_name):
    with open(file_name,'r') as f :
        listings = f.readlines()
    return map(lambda e : e.replace("\n",""),listings)


## Fetch the listings from the API and decode then extract json
def fetch_json_data_from_api(url,string_request,key_string,cleaning_function):
    with HTTPSContextManager(url) as connection:
        connection.request("GET", string_request)
        response = connection.getresponse()
        print response.status, response.reason
        data = response.read()
    # JSON extraction
    results = json.loads(data)['results']
    return [cleaning_function(e[key_string]) for e in results if key_string in e]


def fetch_listings_title_from_api(listings):
    titles = list()
    key_string = 'title'
    url = "openapi.etsy.com"
    string_request = "/v2/listings/:listing_id?api_key=:api_key".replace(":api_key",API_KEYSTRING)
    n = MAX_LISTINGS_LENGTH # Number max of listing_id in the request (avoid too long request string)
    for i in range(len(listings)/n + 1*(len(listings)%n != 0)):
        sub_list = listing_to_querry_string(listings[i*n:n*(i+1)])
        request = string_request.replace(":listing_id",sub_list)
        titles += fetch_json_data_from_api(
            url,
            request,
            key_string,
            title_cleaning)
    return titles

def main():
    #------ Proccess ------#
    # 1 - Listings fecting from file
    # 2 - DATA RETRIEVAL FROM THE API
    # 3 - DATA PROCESSING
    print("Request the API to get the titles")
    class_A = fetch_listings_title_from_api(read_file("listings_A.txt"))
    class_B = fetch_listings_title_from_api(read_file("listings_B.txt"))
    print("Finished fetching data")


    #------ SAVE DATA IN A NEW FILE ------#
    output_A = "titles_A.txt"
    output_B = "titles_B.txt"
    utils.save_in_file(output_A, class_A)
    utils.save_in_file(output_B, class_B)
    # NOTE : Another possibility would be to save (with open in append mode) after every request
    # That would avoid to loop again over the all list and would save some memory
    print("Data saved in files {0} and {1}".format(output_A,output_B))


if __name__ == '__main__':
    main()
