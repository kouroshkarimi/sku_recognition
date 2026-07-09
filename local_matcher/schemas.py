'''
This module defines the Pydantic models for the request and response
schemas used in the local matcher API.
'''
from pydantic import BaseModel

class MatchRequest(BaseModel):
    '''
    MatchRequest is a Pydantic model that defines the request schema for the local matcher API.
    It contains the following fields:
    - query: The path to the query image.
    - candidates: The path to the candidate images.
    '''
    query: str
    candidates: str


class MatchResult(BaseModel):
    '''
    MatchResult is a Pydantic model that defines the response schema for the local matcher API.
    It contains the following fields:
    - query_path: The path to the query image.
    - candidate_path: The path to the candidate image.
    - score: The matching score between the query and candidate images.
    - num_matches: The number of matches found between the query and candidate images.
    - num_inliers: The number of inliers found between the query and candidate images.
    '''
    query_path: str
    candidate_path: str
    score: float
    num_matches: int
    num_inliers: int
