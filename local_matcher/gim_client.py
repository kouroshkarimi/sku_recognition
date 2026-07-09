'''
This module defines the GIMClient class, which is responsible for sending requests
to the GIM service for matching a query image against a set
of candidate images.
The GIMClient class provides a method to send a POST request with the query and candidates,
and returns the response from the GIM service.
'''
import requests

class GIMClient:
    '''
    GIMClient is a client for interacting with the GIM service.
    It provides a method to send a query image and a candidate images.
    '''
    def __init__(self):
        self.url = "http://127.0.0.1:8000/match"

    def match(self, query, candidates):

        payload = {
            "query": str(query),
            "candidates": candidates,
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=60,
        )

        return response
