import streamlit as st
import sqlite3

# Uses SQLite as a database connection
conn = sqlite3.connect('assignments.db')
cursor = conn.cursor()

# Creates a table to store assignments if it doesn't exist yet
cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        due_date DATE,
        priority_level TEXT
    )
''')

# Alter the table to include the "priority_level" column
try:
    cursor.execute('ALTER TABLE assignments ADD COLUMN priority_level TEXT')
    conn.commit()
except sqlite3.OperationalError as e:
    print("Column already exists")

# Main function to insert assignments into the database
def insert_assignment(title, description, due_date, priority_level):
    try:
        query = "INSERT INTO assignments (title, description, due_date, priority_level) VALUES (?, ?, ?, ?)"
        params = (title, description, due_date, priority_level)
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(str(e))

# Function to fetch assignments from the database
def fetch_assignments():
    cursor.execute("SELECT * FROM assignments ORDER BY due_date ASC")
    return cursor.fetchall()

def display_assignments(assignments):
    # Displays the list of assignments
    if len(assignments) > 0:
        
        # Sort assignments by due date in ascending order
        assignments.sort(key=lambda x: x[3])
        
        # Display tasks in a matrix with three tasks side by side
        for i in range(0, len(assignments), 3):
            row_assignments = assignments[i:i + 3]
            cols = st.columns(3)
            for col, assignment in zip(cols, row_assignments):
                col.write(f"**Title:** {assignment[1]}")
                col.write(f"**Description:** {assignment[2]}")
                col.write(f"**Due Date:** {assignment[3]}")
                col.markdown(
                    f"**Priority Level:** <span style='background-color:{assignment[4]}; color:white; padding: 4px; border-radius: 4px;'>  ---  </span>",
                    unsafe_allow_html=True)
                col.write("-----------------------")
    else:
        st.info("No assignments available yet, add one now!")

st.title("Trakr ✒️")
tab1, tab2 = st.tabs(["Add", "Assignments"])

with tab1:
    # Creates a form to add assignments
    st.header("Add Assignment")
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date")

    # Add priority selection using a selectbox with predefined colors
    priority_level = st.selectbox("Select Priority Color", ["Red", "Orange", "Green"])

    # Map the selected priority_level to corresponding color values
    color_mapping = {
        "Red": "#FF0000",
        "Orange": "#FFA500",
        "Green": "#008000"
    }

    if st.button("Add"):
        if title and due_date:
            selected_color = color_mapping.get(priority_level)
            insert_assignment(title, description, due_date, selected_color)
            st.success("Assignment added successfully!")

    def clear_assignments():
        cursor.execute("DELETE FROM assignments")
        conn.commit()


with tab2:
    st.header("Assignments")
    assignments = fetch_assignments()

    # Button to clear assignments
    if st.button("Clear Assignments"):
        clear_assignments()
        st.success("All assignments have been cleared.")

    display_assignments(assignments)