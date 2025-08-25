import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RuleBasedRecommender:
    def __init__(self, embedding_model, zap_file="zaps/zap_database.json"):
        self.embedding_model = embedding_model
        with open(zap_file, "r", encoding="utf-8") as f:
            self.zaps = json.load(f)
        self.templates = [z["title"] if "title" in z else z.get("name", "") for z in self.zaps]
        self.embedding_model.fit(self.templates)
        self.template_matrix = self.embedding_model.transform(self.templates)

    def recommend(self, user_text, top_k=10):
        if not isinstance(user_text, str):
            raise ValueError("user_text must be a string")
        user_matrix = self.embedding_model.transform([user_text])
        scores = cosine_similarity(user_matrix, self.template_matrix).ravel()
        idxs = np.argsort(-scores)[:top_k]
        out = []
        for i in idxs:
            z = self.zaps[i]
            name = z.get("title") or z.get("name") or "Untitled Zap"
            desc = z.get("description", "")
            apps = z.get("apps") or z.get("apps_involved") or []
            url = z.get("zapier_url", "")
            score = float(scores[i])
            out.append({
                "zap": name,
                "description": desc,
                "apps_involved": apps,
                "zapier_url": url,
                "score": round(score, 3),
                "business_value": self.explain_business_value(name)
            })
        return out

    def explain_business_value(self, name):
        n = name.lower()
        if "slack" in n:
            return "Instant team visibility and faster response"
        if "google drive" in n or "onedrive" in n or "dropbox" in n:
            return "Hands-free file organization and backup"
        if "sheet" in n or "excel" in n:
            return "Single source of truth, fewer copy-paste errors"
        if "calendar" in n:
            return "Fewer missed deadlines with automated reminders"
        if "crm" in n or "hubspot" in n or "salesforce" in n:
            return "Improved pipeline hygiene and reporting"
        if "trello" in n or "asana" in n or "jira" in n or "clickup" in n:
            return "Automatic task creation and tighter execution"
        if "github" in n or "gitlab" in n or "discord" in n:
            return "Developer alerts without context switching"
        if "typeform" in n or "form" in n:
            return "Faster data capture and structured logging"
        if "mailchimp" in n or "email" in n or "gmail" in n:
            return "Timely outreach and consistent follow-ups"
        if "twitter" in n or "x " in n or "linkedin" in n:
            return "Consistent outbound distribution without manual posts"
        return "Automates repetitive work to save time and reduce errors"
