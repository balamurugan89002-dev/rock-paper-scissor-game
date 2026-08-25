let pyodide = null;
let pythonReady = false;

const icons = {
    rock: "🪨",
    paper: "📄",
    scissors: "✂️"
};


// =========================
// LOAD PYTHON
// =========================

async function loadPython() {

    const resultBox = document.getElementById("result");

    try {

        resultBox.textContent = "Loading Python... ⏳";

        // Load Pyodide
        pyodide = await loadPyodide();

        resultBox.textContent = "Loading game... ⏳";

        // Load game.py
        const response = await fetch("./game.py");

        if (!response.ok) {
            throw new Error(
                "Could not find game.py. Status: " +
                response.status
            );
        }

        const pythonCode = await response.text();

        // Run game.py
        await pyodide.runPythonAsync(pythonCode);

        pythonReady = true;

        resultBox.textContent =
            "Choose your move! 🎮";

        console.log("Game loaded successfully!");

    } catch (error) {

        console.error("GAME ERROR:", error);

        resultBox.textContent =
            "Game failed to load ❌";

        console.error(error);

    }
}


// =========================
// START GAME
// =========================

function startGame() {

    document.getElementById("start-screen").style.display =
        "none";

    document.getElementById("game-screen").style.display =
        "block";

}


// =========================
// PLAY GAME
// =========================

async function play(choice) {

    if (!pythonReady) {

        document.getElementById("result").textContent =
            "Game is still loading... ⏳";

        return;
    }


    pyodide.globals.set(
        "player_choice",
        choice
    );


    await pyodide.runPythonAsync(`
result = play_game(player_choice)
`);


    const result =
        pyodide.globals.get("result");

    const computerChoice =
        pyodide.globals.get("computer_choice");

    const playerScore =
        pyodide.globals.get("player_score");

    const computerScore =
        pyodide.globals.get("computer_score");


    // Player choice

    document.getElementById("player-icon").textContent =
        icons[choice];

    document.getElementById("player-choice").textContent =
        choice.toUpperCase();


    // Computer choice

    document.getElementById("computer-icon").textContent =
        icons[computerChoice];

    document.getElementById("computer-choice").textContent =
        computerChoice.toUpperCase();


    // Result

    document.getElementById("result").textContent =
        result;


    // Score

    document.getElementById("player-score").textContent =
        playerScore;

    document.getElementById("computer-score").textContent =
        computerScore;


    // Player wins

    if (playerScore >= 10) {

        document.getElementById("result").textContent =
            "🏆 YOU ARE THE CHAMPION! 🎉";

        document.getElementById("final-winner").textContent =
            "Congratulations! You won the match!";

        await pyodide.runPythonAsync(`
player_won()
`);

        disableChoices();

        document.getElementById("try-again").textContent =
            "🆕 NEW GAME";

        return;
    }


    // Computer wins

    if (computerScore >= 10) {

        document.getElementById("result").textContent =
            "🤖 COMPUTER IS THE CHAMPION!";

        document.getElementById("final-winner").textContent =
            "Computer won the match!";

        disableChoices();

        document.getElementById("try-again").textContent =
            "🔄 TRY AGAIN";

        return;
    }

}


// =========================
// DISABLE CHOICES
// =========================

function disableChoices() {

    document
        .querySelectorAll(".choices button")
        .forEach(button => {

            button.disabled = true;

        });

}


// =========================
// RESET GAME
// =========================

async function resetGame() {

    if (!pythonReady) {
        return;
    }


    await pyodide.runPythonAsync(`
reset_game()
`);


    document.getElementById("player-icon").textContent =
        "❔";

    document.getElementById("player-choice").textContent =
        "-";


    document.getElementById("computer-icon").textContent =
        "❔";

    document.getElementById("computer-choice").textContent =
        "-";


    document.getElementById("player-score").textContent =
        "0";

    document.getElementById("computer-score").textContent =
        "0";


    document.getElementById("result").textContent =
        "Choose your move! 🎮";


    document.getElementById("final-winner").textContent =
        "";


    document
        .querySelectorAll(".choices button")
        .forEach(button => {

            button.disabled = false;

        });


    document.getElementById("try-again").textContent =
        "🔄 TRY AGAIN";

}


// =========================
// LOAD GAME
// =========================

loadPython();