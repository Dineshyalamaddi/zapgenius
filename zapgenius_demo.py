import json
from src.embedding_model import EmbeddingModel
from src.recommender import RuleBasedRecommender

def extract_actions(data):
    if isinstance(data, dict) and isinstance(data.get("actions"), list):
        return [str(x) for x in data["actions"]]
    if isinstance(data, list):
        actions = []
        for item in data:
            if isinstance(item, dict):
                parts = []
                for k in ("app_name", "action", "context"):
                    v = item.get(k)
                    if v:
                        parts.append(str(v))
                if parts:
                    actions.append(" ".join(parts))
        if actions:
            return actions
    return ["sending emails", "updating spreadsheets", "creating tasks"]

def main():
    try:
        with open("data/sample_user_data.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        raw = {}
    user_actions = extract_actions(raw)
    embedding_model = EmbeddingModel()
    recommender = RuleBasedRecommender(embedding_model)
    try:
        user_query = input("Describe a task you do frequently (press Enter to use your usage data): ").strip()
    except EOFError:
        user_query = ""
    if user_query:
        user_actions = [user_query]
    recs = recommender.recommend(user_actions, top_k=5)
    print("\n🚀 ZapGenius Recommendations\n")
    print("Based on:", ", ".join(user_actions))
    print("\nTop Results:\n")
    for i, r in enumerate(recs, 1):
        print(f"{i}. {r['zap']}  (score: {r['score']})")
        print(f"   Business Value: {r['business_value']}\n")

if __name__ == "__main__":
    main()
