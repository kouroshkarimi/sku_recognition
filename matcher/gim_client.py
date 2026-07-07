import requests

class GIMClient:

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