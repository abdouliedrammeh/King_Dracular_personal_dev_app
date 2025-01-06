import sqlite3
from datetime import datetime, timedelta


class PersonalDevelopmentApp:
    def __init__(self, db_name="King_Dracular_personal_dev_app.db"):
        self.db_name = db_name
        self.start_database()

    def start_database(self):
        """Initialize the database and update schema if needed."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            deadline DATE,
            progress INTEGER DEFAULT 0,
            total_target INTEGER NOT NULL,
            goal_type TEXT NOT NULL DEFAULT 'General' -- Default to 'General' for backward compatibility
        )
        """)
        # Ensure goal_type column exists (for existing databases)
        cursor.execute("PRAGMA table_info(goals)")
        columns = [col[1] for col in cursor.fetchall()]
        if "goal_type" not in columns:
            cursor.execute("ALTER TABLE goals ADD COLUMN goal_type TEXT NOT NULL DEFAULT 'General'")
        conn.commit()
        conn.close()

    def add_goal(self, goal_type="General"):
        """Add a new goal with optional type (General, Daily, Weekly)."""
        name = input("Enter the goal name: ")
        category = input(
            "Enter the category (e.g., Fitness, Learning, Mindfulness, Religion, Cooking, Skincare, Screentime, Hobby): ")
        deadline = input("Enter the deadline (YYYY-MM-DD) or leave blank: ")
        total_target = int(input("Enter the total target value (e.g., number of sessions, number of prayers etc.): "))

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO goals (name, category, deadline, total_target, goal_type)
        VALUES (?, ?, ?, ?, ?)
        """, (name, category, deadline or None, total_target, goal_type))
        conn.commit()
        conn.close()
        print(f"{goal_type} goal added successfully!")

    def view_goals(self):
        """View all goals in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals")
        goals = cursor.fetchall()
        conn.close()

        if not goals:
            print("No goals found.")
        else:
            print("\nCurrent Goals:")
            for goal in goals:
                print(
                    f"ID: {goal[0]}, Name: {goal[1]}, Category: {goal[2]}, "
                    f"Deadline: {goal[3] or 'N/A'}, Progress: {goal[4]}/{goal[5]}, Type: {goal[6]}"
                )

    def update_progress(self):
        """Update progress for a specific goal."""
        goal_id = int(input("Enter the ID of the goal to update: "))
        progress_increment = int(input("Enter the progress amount to add: "))

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE goals SET progress = progress + ? WHERE id = ?", (progress_increment, goal_id))
        conn.commit()
        conn.close()
        print("Progress updated successfully!")

    def delete_goal(self):
        """Delete a goal based on its ID."""
        goal_id = int(input("Enter the ID of the goal to delete: "))
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()
        conn.close()
        print("Goal deleted successfully!")

    def add_daily_goal(self):
        """Shortcut to add a daily goal."""
        self.add_goal(goal_type="Daily")

    def add_weekly_goal(self):
        """Shortcut to add a weekly goal."""
        self.add_goal(goal_type="Weekly")

    def main_menu(self):
        """Display the main menu."""
        while True:
            print("\n--- King Dracular Personal Development App ---")
            print("1. Add a General Goal")
            print("2. Add a Daily Goal")
            print("3. Add a Weekly Goal")
            print("4. View Goals")
            print("5. Update Progress")
            print("6. Delete a Goal")
            print("7. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_goal()
            elif choice == '2':
                self.add_daily_goal()
            elif choice == '3':
                self.add_weekly_goal()
            elif choice == '4':
                self.view_goals()
            elif choice == '5':
                self.update_progress()
            elif choice == '6':
                self.delete_goal()
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = PersonalDevelopmentApp()
    app.main_menu()


class Analytics:
    pass