import os

class Leaderboard:
    def __init__(self, file_path="leaderboard.txt", max_entries=5):
        """
        Initialize the leaderboard system.
        :param file_path: Path to the file where leaderboard data is stored.
        :param max_entries: Maximum number of leaderboard entries to keep.
        """
        self.file_path = file_path
        self.max_entries = max_entries
        self.scores = self.load_scores()

    def load_scores(self):
        """Load the leaderboard scores from the file."""
        if not os.path.exists(self.file_path):
            return []  # Return an empty list if the file doesn't exist

        with open(self.file_path, "r") as file:
            lines = file.readlines()

        scores = []
        for line in lines:
            try:
                initials, score = line.strip().split(",")
                scores.append((initials, int(score)))
            except ValueError:
                continue  # Skip malformed lines

        # Sort scores in descending order
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def save_scores(self):
        """Save the leaderboard scores to the file."""
        with open(self.file_path, "w") as file:
            for initials, score in self.scores:
                file.write(f"{initials},{score}\n")

    def add_score(self, initials, score):
        """
        Add a new score to the leaderboard.
        :param initials: Player initials.
        :param score: Player score.
        """
        self.scores.append((initials, score))
        # Sort scores in descending order and keep only the top entries
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)[:self.max_entries]
        self.save_scores()

    def qualifies_for_leaderboard(self, score):
        """
        Check if a score qualifies for the leaderboard.
        :param score: The score to check.
        :return: True if the score qualifies, False otherwise.
        """
        if len(self.scores) < self.max_entries:
            return True  # Automatically qualifies if there are fewer than max entries
        return score > self.scores[-1][1]  # Qualifies if it's higher than the lowest score

    def display_leaderboard(self):
        """Display the leaderboard."""
        print("LEADERBOARD:")
        for rank, (initials, score) in enumerate(self.scores, start=1):
            print(f"{rank}. {initials} - {score}")