Rock Paper Scissors Game

Project Overview

A simple Rock Paper Scissors game built as a beginner-friendly web project. The player chooses Rock, Paper, or Scissors, and the computer makes a random choice. Python handles the core game logic through Pyodide, while HTML, CSS, and JavaScript provide the browser interface and interaction.

Objective

Build an interactive Rock Paper Scissors game that demonstrates:

- User input
- Random choices
- Conditional statements
- Functions
- Python programming
- Event handling
- DOM manipulation
- Communication between Python and JavaScript
- Updating webpage content

Workflow

1. The player selects Rock, Paper, or Scissors.
2. JavaScript captures the player's button selection.
3. The selected value is passed to the Python game logic running through Pyodide.
4. Python generates the computer's random choice.
5. Python compares the player and computer choices.
6. Python determines whether the result is Win, Lose, or Draw.
7. The result and score are returned to the webpage.
8. JavaScript updates the displayed result and score.
9. The player can continue playing.

Python Usage

Python is used for the main game logic of the project.

Python handles:

- Computer choice generation
- Rock Paper Scissors game rules
- Win/Lose/Draw calculation
- Score management
- Game functions and variables
- Processing the player's choice

The Python code runs directly in the browser using Pyodide, which provides a Python runtime based on WebAssembly.

This allows the project to use Python without requiring a separate Python server.

Python + Pyodide Workflow

Player → JavaScript → Pyodide → Python → JavaScript → Webpage

- JavaScript receives the player's input.
- Pyodide runs the Python code inside the browser.
- Python processes the game logic.
- The result is sent back to JavaScript.
- JavaScript updates the webpage.

Tech Stack

HTML

Used to create the structure of the game page, including buttons, headings, score areas, and result sections.

CSS

Used to design the game interface, including layout, spacing, colors, buttons, and responsive styling.

Python

Used for the main Rock Paper Scissors game logic, including random computer choices, game rules, result calculation, and score handling.

Pyodide

Used to run Python directly inside the web browser. It connects the Python game logic with the browser environment.

JavaScript

Used as the browser-side integration layer. JavaScript handles:

- Button/event interactions
- Passing player input to Python
- Calling Python through Pyodide
- Receiving Python results
- Updating the DOM

Git & GitHub

Git is used for version control, while GitHub is used to store the project repository online.

GitHub Pages

GitHub Pages is used to host the game so it can be accessed through a public web URL.

How the Tech Stack Works Together

HTML → CSS → JavaScript → Pyodide → Python → Git/GitHub → GitHub Pages

- HTML creates the webpage structure.
- CSS styles the interface.
- JavaScript handles browser interaction.
- Pyodide runs Python inside the browser.
- Python handles the game logic.
- Git tracks project changes.
- GitHub stores the project repository.
- GitHub Pages publishes the project on the web.

Hosting

The game is hosted using GitHub Pages.

Item| Details
Hosting Platform| GitHub Pages
Repository| "balamurugan89002-dev/rock-paper-scissors"
Live Site| "https://balamurugan89002-dev.github.io/rock-paper-scissors/"

If your repository name or GitHub Pages URL is different, replace the values above with the details shown in your GitHub Pages settings.

Technologies Used

Technology| Purpose
HTML| Webpage structure
CSS| Styling and responsive design
JavaScript| Browser interaction and Pyodide integration
Python| Game logic and score management
Pyodide| Runs Python in the browser
Git| Version control
GitHub| Repository hosting
GitHub Pages| Website hosting

Key Concepts Learned

- Python variables
- Python functions
- Conditional statements
- Random number generation
- JavaScript event handling
- DOM manipulation
- Python and JavaScript integration
- Pyodide
- Basic web design
- Git and GitHub
- Website deployment

Conclusion

This Rock Paper Scissors game combines Python programming with web development. Python handles the core game logic through Pyodide, while HTML, CSS, and JavaScript create the browser interface and interaction. The project provides practical experience with Python, JavaScript, Pyodide, Git, GitHub, and GitHub Pages.
