from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from matcher.model_loader import ModelLoader
from matcher.matcher import GIMMatcher


loader = ModelLoader()
matcher = GIMMatcher(loader)

match_result = matcher.match(
    query_path="assets/h3.jpg",
    candidate_path="assets/h1.jpg",
)


print(match_result.score)
print(match_result.num_matches)
print(match_result.num_inliers)