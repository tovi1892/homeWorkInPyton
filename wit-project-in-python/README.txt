# CodeGuard & WIT - Version Control & Code Analysis System

## General Description
This project is a basic version control system (VCS) inspired by Git (WIT), integrated with a CodeGuard CI server that automatically analyzes Python files for code quality and generates visual reports when pushing code.

## Requirements
To run this project, you need to install the following libraries:
- click
- requests
- fastapi
- uvicorn
- python-multipart
- matplotlib

You can install them using:
pip install click requests fastapi uvicorn python-multipart matplotlib

## How to Run

### 1. Start the CI Server (First Terminal):
python -m uvicorn server.main:app --reload

### 2. Run WIT Commands (Second Terminal - inside `client` directory):
Navigate to the client folder first: `cd client`

1. Initialize a repository:
   python wit.py init

2. Add files to staging:
   python wit.py add <file_path>
   (Example: python wit.py add test.py)

3. Create a commit:
   python wit.py commit -m "your message"

4. Check status:
   python wit.py status

5. Checkout a commit:
   python wit.py checkout <commit_id>

6. Push & Analyze Code (New ✨):
   python wit.py push

## Project Structure
- client/wit.py: The CLI entry point.
- client/core.py: The core logic of the system and push mechanism.
- server/main.py: FastAPI server entry point.
- server/analyzer.py: AST static code analysis rules.
- server/visualizer.py: Matplotlib graph generator.
- .wit/: Metadata and storage directory.

## Example Usage Scenario
1. Start the server using `python -m uvicorn server.main:app --reload`.
2. Open a new terminal, go to client folder `cd client`, and run `python wit.py init`.
3. Create or update a Python file (e.g., `test.py`) and run `python wit.py add test.py`.
4. Run `python wit.py commit -m "Testing push"` to save.
5. Run `python wit.py push` to get code quality warnings and automatically generate your graph image (`graph_test.py.png`).
