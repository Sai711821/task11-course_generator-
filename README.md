Course Generator Project

This project is a Python-based tool that leverages OpenAI's GPT-4 model to generate a table of contents for courses based on a given description, subject, and difficulty level. It stores the generated course details in a SQLite database for future reference.

Install Dependencies:
pip install openai

Features

Course Chapter Generation: Automatically generates a structured table of contents for courses based on user-provided input.

Database Integration: Stores course descriptions, subjects, levels, generated tables of contents, and timestamps in a SQLite database.

Simple CLI Interface: User-friendly command-line interface to input data and display results.

How It Works

User inputs a course description, subject, and level (Beginner, Intermediate, or Advanced).

The program sends the input to OpenAI's GPT-4 model to generate a table of contents.

The generated content is displayed to the user and saved in a SQLite database.

Technologies Used

Python: Programming language used for the implementation.

SQLite: Lightweight database to store course details.

OpenAI GPT-4 API: Used for generating the course content.

Requirements

Python 3.10 or higher

OpenAI Python SDK

SQLite


