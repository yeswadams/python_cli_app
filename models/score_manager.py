from utils.storage import load_json_list, save_json_list


class ScoreManager:
    def __init__(self, scores_file="data/scores.json", max_scores: int = 10):
        self.scores_file = scores_file
        self.max_scores = max_scores
        self.scores = self.load_scores()

    def load_scores(self):
        return load_json_list(self.scores_file)
    
    def save_scores(self):
        save_json_list(self.scores_file, self.scores)
             
    def add_score(self, player_name, score):
        self.scores.append({"name": player_name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:self.max_scores]
        self.save_scores()

    def display_scores(self):
        if not self.scores:
            print("No scores yet.")
        else:
            print("\nHigh Scores:")
            for idx, entry in enumerate(self.scores, 1):
                print(f"{idx}. {entry['name']} - {entry['score']}")
