import sqlite3
from datetime import datetime

# Database setup
def start_database():
    conn = sqlite3.connect("King_Dracular_personal_dev_app.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        deadline DATE,
        progress INTEGER DEFAULT 0,
        total_target INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Add a new goal
def add_goal():
    name = input("Enter the goal name: ")
    category = input("Enter the category (e.g., Fitness, Learning, Mindfulness, Religion, Cooking, Skincare, Screentime,Hobby): ")
    deadline = input("Enter the deadline (YYYY-MM-DD) or leave blank: ")
    total_target = int(input("Enter the total target value (e.g., number of sessions, number of prayers, etc. ): "))

    conn = sqlite3.connect("King_Dracular_personal_dev_app.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO goals (name, category, deadline, total_target)
    VALUES (?, ?, ?, ?)
    """, (name, category, deadline or None, total_target))
    conn.commit()
    conn.close()
    print("Goal added successfully!")

# View all goals
def view_goals():
    conn = sqlite3.connect("King_Dracular_personal_dev_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals")
    goals = cursor.fetchall()
    conn.close()

    if not goals:
        print("No goals found.")
    else:
        print("\nCurrent Goals:")
        for goal in goals:
            print(f"ID: {goal[0]}, Name: {goal[1]}, Category: {goal[2]}, Deadline: {goal[3] or 'N/A'}, Progress: {goal[4]}/{goal[5]}")

# Update progress for a goal
def update_progress():
    goal_id = int(input("Enter the ID of the goal to update: "))
    progress_increment = int(input("Enter the progress amount to add: "))

    conn = sqlite3.connect("King_Dracular_personal_dev_app.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE goals SET progress = progress + ? WHERE id = ?", (progress_increment, goal_id))
    conn.commit()
    conn.close()
    print("Progress updated successfully!")

# Main menu
def main_menu():
    start_database()
    while True:

    
        print("\n--- King Dracular personal dev app ---")
        print("1. Add a Goal")
        print("2. View Goals")
        print("3. Update Progress")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_goal()
        elif choice == '2':
            view_goals()
        elif choice == '3':
            update_progress()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
