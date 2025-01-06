import pytest
import sqlite3
from King_Dracular_personal_dev_app import PersonalDevelopmentApp, Analytics


@pytest.fixture
def setup_test_environment():
    """Setup an in-memory database for testing."""
    app = PersonalDevelopmentApp(":memory:")
    analytics = Analytics(":memory:")

    # Insert sample data
    conn = sqlite3.connect(app.db_name)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO goals (name, description, progress, type)
        VALUES (?, ?, ?, ?)
    """, [
        ("Exercise", "Daily exercise routine", 50, "Daily"),
        ("Study", "Complete Python tutorials", 30, "General"),
        ("Code", "Build a project", 100, "General"),
    ])
    conn.commit()
    conn.close()

    return app, analytics


def test_add_goal(setup_test_environment):
    """Test adding a new goal."""
    app, _ = setup_test_environment
    app.add_goal("Read", "Read 20 pages", "Daily")

    conn = sqlite3.connect(app.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE name = 'Read'")
    goal = cursor.fetchone()
    conn.close()

    assert goal is not None
    assert goal[1] == "Read"
    assert goal[2] == "Read 20 pages"
    assert goal[3] == 0  # Default progress
    assert goal[4] == "Daily"


def test_update_progress(setup_test_environment):
    """Test updating the progress of an existing goal."""
    app, _ = setup_test_environment

    # Get the ID of the "Exercise" goal
    conn = sqlite3.connect(app.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM goals WHERE name = 'Exercise'")
    goal_id = cursor.fetchone()[0]
    conn.close()

    app.update_progress(goal_id, 20)  # Update progress by 20

    conn = sqlite3.connect(app.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT progress FROM goals WHERE id = ?", (goal_id,))
    updated_progress = cursor.fetchone()[0]
    conn.close()

    assert updated_progress == 70  # 50 (initial) + 20 (updated)


def test_delete_completed_goals(setup_test_environment):
    """Test deleting goals with 100% or more progress."""
    app, _ = setup_test_environment
    app.delete_completed_goals()

    conn = sqlite3.connect(app.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE progress >= 100")
    completed_goals = cursor.fetchall()
    conn.close()

    assert len(completed_goals) == 0  # All completed goals should be deleted


def test_total_tracked_goals(setup_test_environment):
    """Test calculating the total number of tracked goals."""
    _, analytics = setup_test_environment
    total_goals = analytics.total_tracked_goals()
    assert total_goals == 3  # Initial 3 goals added


def test_analytics_average_progress(setup_test_environment):
    """Test calculating the average progress across all goals."""
    _, analytics = setup_test_environment
    average_progress = analytics.average_progress()
    assert average_progress == 60  # (50 + 30 + 100) / 3
