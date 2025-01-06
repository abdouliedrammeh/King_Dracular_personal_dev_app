import sqlite3
from datetime import datetime

class Analytics:
    def __init__(self, db_name="King_Dracular_personal_dev_app.db"):
        self.db_name = db_name

    def get_all_habits(self):
        """Retrieve all habits from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals")
        habits = cursor.fetchall()
        conn.close()
        return habits

    def list_habits_by_periodicity(self, periodicity):
        """List all habits with the same periodicity."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals WHERE goal_type = ?", (periodicity,))
        habits = cursor.fetchall()
        conn.close()
        return habits

    def longest_streak(self, habit_name):
        """
        Calculate the longest streak for a given habit.
        Assuming `progress` increments represent consistent daily progress.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT progress, total_target FROM goals WHERE name = ?", (habit_name,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return f"No habit found with name: {habit_name}"

        progress, total_target = data
        streak = progress // total_target if total_target else 0
        return streak

    def all_streaks(self):
        """Calculate streaks for all habits."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, progress, total_target FROM goals")
        data = cursor.fetchall()
        conn.close()

        streaks = {}
        for name, progress, total_target in data:
            streak = progress // total_target if total_target else 0
            streaks[name] = streak
        return streaks

    def sum_and_average(self, category):
        """
        Calculate the sum and average of progress for all habits in a given category.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT progress FROM goals WHERE category = ?", (category,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            return f"No habits found in category: {category}"

        progress_values = [row[0] for row in data]
        total_sum = sum(progress_values)
        average = total_sum / len(progress_values)
        return {"sum": total_sum, "average": average}

# Example Usage
if __name__ == "__main__":
    analytics = Analytics()

    print("--- All Habits ---")
    print(analytics.get_all_habits())

    print("\n--- Habits by Periodicity: Daily ---")
    print(analytics.list_habits_by_periodicity("Daily"))

    print("\n--- Longest Streak for 'Exercise' ---")
    print(analytics.longest_streak("Exercise"))

    print("\n--- All Streaks ---")
    print(analytics.all_streaks())

    print("\n--- Sum and Average for Category: Fitness ---")
    print(analytics.sum_and_average("Fitness"))
