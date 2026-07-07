from pydantic import BaseModel


class MatchRequest(BaseModel):
    query: str
    candidates: str


class MatchResult(BaseModel):
    query_path: str
    candidate_path: str
    score: float
    num_matches: int
    num_inliers: int


