from openai import OpenAI
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

# Retrieve the API key from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set it in the .env file.")


#initializing the cchatgpt client
client = OpenAI(api_key=api_key)

#initializing the sqlite3 databse setup to save responses using queries and cursor
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

#Modular Function to generate a table of contents using chatgpt API
def generate_table_of_contents(description, subject, level):
    messages = [
        {"role": "user", "content": f"Create a table of contents for a course with the following details:\nDescription: {description}\nSubject: {subject}\nLevel: {level}"}
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=messages
    )
    return completion.choices[0].message.content.strip()


#another function to save course details in the database
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
    setup_database()
    print("Welcome to the Course Chapter Generator!")
    
    
    description = os.getenv("COURSE_DESCRIPTION")
    subject = os.getenv("COURSE_SUBJECT")
    level = os.getenv("COURSE_LEVEL")
    print("\nGenerating the table of contents...\n")
    table_of_contents = generate_table_of_contents(description, subject, level)

    print("Table of Contents:\n")
    print(table_of_contents)

    save_course_to_db(description, subject, level, table_of_contents)
    print("\nCourse details saved to the database!")


main()

#Sample input for testing
# Description: Exploring quantum computing fundamentals and its potential applications.
# Subject: Quantum Computing.
# Level: Intermediate.

# Description: Introduction to Python programming.
# Subject: Python.
# Level: Beginner.