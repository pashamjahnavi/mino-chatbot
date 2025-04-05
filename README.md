# Mino - Your Personal AI Assistant

## Overview
Mino is an intelligent chatbot application built with Streamlit and powered by the BlenderBot model. It provides a modern, user-friendly interface for interactive conversations with an AI assistant.

## Features
- 🔐 **Secure Authentication**: User login and signup system with password hashing
- 👤 **Profile Customization**: Upload and display profile pictures
- 💬 **Interactive Chat Interface**: Modern chat UI with message history
- 🎨 **Beautiful Design**: Clean and responsive interface with custom styling
- 🔄 **Session Management**: Persistent chat sessions with timestamp tracking
- 🚪 **Easy Navigation**: Intuitive navigation between home, login, and chat pages

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **AI Model**: OPENAI_API_KEY=sk-Abc123xYz789DefGhi456JklMno0PqRsTuVwXyZ
- **Authentication**: SHA-256 hashing
- **Image Processing**: PIL (Python Imaging Library)

## Prerequisites
- Python 3.8+
- MySQL Server
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mino-chatbot.git
cd mino-chatbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add your configuration:
```
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=mino_db
OPENAI_API_KEY=your_api_key
```

4. Set up the database:
```sql
CREATE DATABASE mino_db;
USE mino_db;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

5. Run the application:
```bash
streamlit run app.py
```

## Project Structure
```
mino-chatbot/
├── app.py              # Main application entry point
├── views/
│   ├── __init__.py    # Views initialization
│   ├── chatbot.py     # Chat interface logic
│   ├── home.py        # Home page view
│   └── login.py       # Authentication views
├── ai.jpg             # AI assistant avatar
├── my.mp4             # Welcome video
├── db_config.py       # Database configuration
├── .env               # Environment variables
└── README.md          # Project documentation
```

## Usage
1. Start by creating an account or logging in
2. Optionally upload a profile picture during signup/login
3. Begin chatting with Mino in the interactive chat interface
4. View chat history in the sidebar
5. Clear chat or logout using the provided buttons

## Security Features
- Password hashing using SHA-256
- Secure session management
- Protected routes requiring authentication
- Safe image handling and storage

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 