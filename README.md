# TeleStudentAssistant

TeleStudentAssistant is a multi-agent AI student assistant that works through Telegram.

## What is it?

It helps students manage their academic activities and get AI-based learning support in one place.

## Main Features

- Manage student information
- Add and view subjects
- Manage assignments
- Track exams
- Generate study plans
- Generate quizzes
- Answer study questions using AI
- Show study progress
- Summarize PDF notes
- Validate inputs and outputs

## Multi-Agent System

The project uses five agents:

1. **Frontend Agent** – Handles student communication.
2. **Backend Agent** – Coordinates tasks between agents.
3. **Database Agent** – Stores and retrieves student data.
4. **Response Agent** – Generates AI responses and study content.
5. **Security Agent** – Checks inputs and outputs for safety.

## Technologies Used

- Python
- Telegram Bot API
- Ollama
- Llama 3.2
- SQLite
- PyMuPDF
- APScheduler
- Git & GitHub

## Architecture

Student → Telegram → Frontend Agent → Security Agent → Backend Agent → Database / Response Agent → Student

## AI

The project uses **Ollama with Llama 3.2** to generate local AI responses.

## Database

SQLite is used to store:

- Student information
- Subjects
- Assignments
- Exams
- Study history
- Quiz results

## PDF Processing

PDF notes are processed using PyMuPDF.  
The extracted text is given to the local AI model to generate a summary.

## Project Purpose

The main purpose of this project is to provide students with a simple, centralized assistant for academic management and learning support.

## Future Enhancements

- Voice message support
- Better automatic reminders
- Interactive quizzes
- Improved PDF processing
- Personalized learning recommendations
- Web dashboard

## Author

**Sanjay R**

B.Tech Artificial Intelligence and Data Science
