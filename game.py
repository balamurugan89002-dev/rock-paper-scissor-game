import random


# =========================
# GAME SETTINGS
# =========================

choices = ["rock", "paper", "scissors"]

player_score = 0
computer_score = 0
computer_choice = ""

player_history = []

WINNING_SCORE = 10


# =========================
# DIFFICULTY
# =========================

# Level 1 = Easy
# Level 2 = Normal
# Level 3 = Hard
# Level 4 = Very Hard

difficulty_level = 1


# =========================
# COMPUTER CHOICE
# =========================

def get_computer_choice():

    # LEVEL 1 - EASY
    if difficulty_level == 1:

        return random.choice(choices)


    # LEVEL 2 - NORMAL
    if difficulty_level == 2:

        if len(player_history) < 2:
            return random.choice(choices)

        most_used = max(
            choices,
            key=player_history.count
        )

        counter = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }

        # 60% chance to counter
        if random.random() < 0.6:
            return counter[most_used]

        return random.choice(choices)


    # LEVEL 3 - HARD
    if difficulty_level == 3:

        if len(player_history) < 2:
            return random.choice(choices)

        most_used = max(
            choices,
            key=player_history.count
        )

        counter = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }

        # 80% chance to counter
        if random.random() < 0.8:
            return counter[most_used]

        return random.choice(choices)


    # LEVEL 4 - VERY HARD
    if difficulty_level >= 4:

        if len(player_history) < 2:
            return random.choice(choices)

        last_move = player_history[-1]

        counter = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }

        # 90% chance to counter
        if random.random() < 0.9:
            return counter[last_move]

        return random.choice(choices)


# =========================
# PLAY GAME
# =========================

def play_game(player_choice):

    global player_score
    global computer_score
    global computer_choice

    # Computer chooses
    computer_choice = get_computer_choice()

    # Remember player's move
    player_history.append(player_choice)


    # =========================
    # DRAW
    # =========================

    if player_choice == computer_choice:

        return "It's a Draw! 🤝"


    # =========================
    # PLAYER WINS ROUND
    # =========================

    if (
        (player_choice == "rock"
         and computer_choice == "scissors")

        or

        (player_choice == "paper"
         and computer_choice == "rock")

        or

        (player_choice == "scissors"
         and computer_choice == "paper")
    ):

        player_score += 1

        if player_score >= WINNING_SCORE:
            return "🏆 YOU ARE THE CHAMPION!"

        return "You Win! 🎉"


    # =========================
    # COMPUTER WINS ROUND
    # =========================

    computer_score += 1

    if computer_score >= WINNING_SCORE:
        return "🤖 COMPUTER IS THE CHAMPION!"

    return "You Lose! 😢"


# =========================
# RESET MATCH
# =========================

def reset_game():

    global player_score
    global computer_score
    global computer_choice
    global player_history

    player_score = 0
    computer_score = 0
    computer_choice = ""

    # Reset moves for the new match
    player_history = []

    # IMPORTANT:
    # difficulty_level is NOT reset here.
    #
    # If you lose:
    # Same difficulty remains.
    #
    # If you win:
    # player_won() increases difficulty.


# =========================
# PLAYER WON
# MAKE COMPUTER HARDER
# =========================

def player_won():

    global difficulty_level

    if difficulty_level < 4:
        difficulty_level += 1


# =========================
# GET CURRENT DIFFICULTY
# =========================

def get_difficulty():

    return difficulty_level