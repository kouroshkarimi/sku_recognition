"""
Image matching server using FastAPI. 

This server exposes an endpoint to match a query image against
a set of candidate images using the GIM matcher.
"""

from fastapi import FastAPI
from local_matcher.schemas import MatchRequest, MatchResult
from local_matcher.model_loader import ModelLoader
from local_matcher.matcher import GIMMatcher


app = FastAPI(
    title="GIM Image Matching Service",
    version="1.0"
)


# Load model only once
print("Initializing GIM matcher...")
loader = ModelLoader()
matcher = GIMMatcher(loader=loader)
print("GIM matcher ready")



@app.post("/match", response_model=MatchResult)
def match(request: MatchRequest):
    '''
    Match a query image against a set of candidate images.
    Args:
        request (MatchRequest object): The request body containing the query image path
                                and candidate image paths.
    Returns:
        MatchResult object: The result of the matching process.
    '''
    result = matcher.match(
        query_path=request.query,
        candidate_path=request.candidates
    )

    return result



@app.get("/health")
def health():
    '''
    Check the health of the server.
    '''
    return {
        "status": "ok"
    }
