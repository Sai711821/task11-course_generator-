import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import openai  # Corrected import

# Load environment variables
load_dotenv()

# Retrieve the API key from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set it in the .env file.")

# Initialize the SQLite database setup
def setup_database():
    conn = sqlite3.connect("course_generator.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            subject TEXT,
            level TEXT,
            table_of_contents TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()

# Modular function to generate a table of contents using OpenAI API
def generate_table_of_contents(description, subject, level):
    messages = [
        {"role": "user", "content": f"Create a table of contents for a course with the following details:\nDescription: {description}\nSubject: {subject}\nLevel: {level}"}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return completion.choices[0].message.content.strip()

# Function to save course details in the database
def save_course_to_db(description, subject, level, table_of_contents):
    conn = sqlite3.connect("course_generator.db")
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute("""
        INSERT INTO courses (description, subject, level, table_of_contents, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (description, subject, level, table_of_contents, timestamp))
    conn.commit()
    conn.close()

# Main function to handle user input and display results
def main():
    # Ensure the database is set up before any operations
    setup_database()

    # Retrieve values from environment variables
    description = os.getenv("COURSE_DESCRIPTION")
    subject = os.getenv("COURSE_SUBJECT")
    level = os.getenv("COURSE_LEVEL")

    if not (description and subject and level):
        raise ValueError("Missing one or more required environment variables.")

    print(f"Description: {description}")
    print(f"Subject: {subject}")
    print(f"Level: {level}")

    # Generate the course
    print("\nGenerating the table of contents...\n")
    table_of_contents = generate_table_of_contents(description, subject, level)
    print("Table of Contents:")
    print(table_of_contents)

    # Save to the database
    save_course_to_db(description, subject, level, table_of_contents)
    print("\nCourse details saved to the database!")

if __name__ == "__main__":
    main()
