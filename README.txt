ROCK-PAPER-SCISSORS ARENA

1. PROJECT SUMMARY
This project is a web-based Rock-Paper-Scissors game developed with the support of GitHub Copilot, featuring database connectivity and a modern user interface.

2. TECHNOLOGIES USED
- Backend: Python (Flask Framework)
- Database: SQLite (With automatic table creation logic)
- Frontend: HTML5 + Tailwind CSS (via CDN)
- Extra: canvas-confetti library (For visual effects)
- Development Environment: VS Code + GitHub Copilot Agent

3. COPILOT USAGE PROCESS
The entire project was developed within VS Code using the GitHub Copilot "Agent" mode.
- Backend Structure: Flask routes and the SQLite database schema (table structure, data recording) were created by providing prompts to Copilot.
- Design: A modern interface was achieved by describing Tailwind CSS classes to Copilot (e.g., "Make it centered, large buttons, responsive").
- Error Resolution: Version errors encountered during development (such as Flask before_first_request, etc.) were resolved by pasting them into Copilot Chat.
- Enhancements: Confetti effects and button animations were added to the project upon completion, again through Copilot guidance.

4. INSTALLATION AND EXECUTION
1. Navigate to the project folder.
2. Install the necessary libraries: pip install -r requirements.txt
3. Start the application: python app.py
4. Go to http://127.0.0.1:5000 in your browser.