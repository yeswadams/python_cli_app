# score_manager
import json
import os

class ScoreManager:
    def __init__(self, scores_file="data/scores.json", max_scores: int=10):
        self.scores_file = scores_file
        self.max_scores = max_scores
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_scores(self):
        with open(self.scores_file, "w") as f:
            json.dump(self.scores, f, indent=4)
             
    def add_score(self, player_name, score):
        self.scores.append({"name":player_name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:self.max_scores]
        self.save_scores()   
    def display_scores(self):
        if not self.scores:
            print("No scores yet.") 
        else:
            print("\nHign Scores:")  
            for idx, entry in enumerate(self.scores,1):
                print(f"{idx}. {entry['name']} - {entry['score']}")     

        
