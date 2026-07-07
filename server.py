from fastapi import FastAPI

from matcher.schemas import MatchRequest
from service import find_best_match

app = FastAPI()


@app.post("/match")
def match(request: MatchRequest):

    result = find_best_match(
        request.query,
        request.candidates,
    )

    return result