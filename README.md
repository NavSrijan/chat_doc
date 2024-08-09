# Chat Doc
## Overview

Chat Doc is a chatbot application developed using Streamlit and Gemini's Generative AI model. The bot enables users to chat with an AI, upload files (PDF, TXT, DOCX) for content extraction, and maintains chat history along with user authentication.
Project Structure

- main.py: The main entry point of the application. It handles the user interface, chat interactions, and session management.

- functions.py: Contains helper functions such as password hashing, file handling (PDF, TXT, DOCX), and conversion utilities for chat history.

- db.py: Manages the database connection and CRUD operations for different tables (Users, Messages, Chats, Attachments).

## Key Features

- User Authentication:
    - Users can register or log in using a simple username and password.
    - Passwords are securely stored using bcrypt hashing.

- Chat Functionality:
    - Users can interact with the chatbot, which is powered by Gemini's Generative AI model.
    - Chat history is maintained for each user, enabling seamless conversation continuity.

- File Upload and Processing:
    - Users can upload files (PDF, TXT, DOCX) to the chat.
    - The content of the uploaded file is extracted and sent to the chatbot for processing.
    - The bot can understand and respond to the content of the uploaded files.

- Database Management:
    - User data, messages, chats, and file attachments are stored in a PostgreSQL database.
    - The database is accessed through a set of custom classes (Users, Messages, Chats, Attachments) which handle various CRUD operations.

## Detailed Code Explanation
- main.py

    - Session State Initialization: Initializes session states for various objects like Users, Messages, Chats, Attachments, and more.

    - User Authentication: The check_password() function checks whether the user is registered or logs in using the correct credentials. If not, the user is prompted to log in or register.

    - Chat Interface: The main chat interface is created with a title, sidebar options, and chat input. Users can switch between different chats or start a new one. Uploaded files are handled, and their content is processed by the AI model.

    - Chat History: The chat history is displayed using st.chat_message for both user and assistant roles.

- functions.py

    - Password Hashing & Verification: Functions like hash_pwd and check_hash ensure secure password management.

    - File Handling: Functions like handle_file, extract_text_from_pdf, extract_text_from_txt, and extract_text_from_docx handle different file types and extract text content for the AI model to process.

    - Conversion Utilities: convert_to_dict_format and convert_to_history help convert chat data between different formats (e.g., from a list of dictionaries to a string format).

    - AI Integration: The Gen_chat class handles interaction with Gemini's Generative AI model, including initiating a chat session and sending messages.

- db.py

    - Database Connection: The Database class and its derived classes (Users, Messages, Chats, Attachments) manage the connection to a PostgreSQL database.

    - CRUD Operations: These classes handle all necessary CRUD operations like adding users, fetching messages, managing chats, and storing file attachments.

    - Decorator _is_connected: Ensures that the database connection is open before any operation and closes the connection afterward.

- Setup and Installation

    - Prerequisites:
        Python 3.8+
        PostgreSQL Database
        Necessary Python libraries (streamlit, bcrypt, PyPDF2, python-docx, psycopg2, google.generativeai)

    - Installation:
        1. Clone the repository.
        2. Install the required dependencies using pip install -r requirements.txt.
        3. Set up the PostgreSQL database and create the necessary tables using the provided SQL schema.
        4. Set environment variables for the database connection and the Gemini API key.

    - Running the Application:
        1. Start the Streamlit app using streamlit run main.py.
        2. Access the application in your browser and interact with the chatbot.

## Conclusion

Chat Doc is a robust and user-friendly chatbot application designed to help users interact with AI, manage chat histories, and process uploaded files. With secure user authentication and a well-structured database, it serves as a reliable tool for various use cases.
