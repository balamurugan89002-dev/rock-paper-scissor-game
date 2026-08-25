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
# COUNTER MOVES
# =========================

counter = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}


# =========================
# GET MOST USED MOVE
# =========================

def get_most_used_move():

    if not player_history:
        return random.choice(choices)

    return max(
        choices,
        key=player_history.count
    )


# =========================
# PREDICT PLAYER MOVE
# =========================

def predict_player_move():

    if not player_history:
        return random.choice(choices)


    # ---------------------------------
    # Look at recent moves
    # ---------------------------------

    recent_moves = player_history[-5:]


    # Count recent moves

    recent_counts = {
        move: recent_moves.count(move)
        for move in choices
    }


    most_recent_used = max(
        recent_counts,
        key=recent_counts.get
    )


    # ---------------------------------
    # Detect repeated move
    # ---------------------------------

    if len(player_history) >= 3:

        last_three = player_history[-3:]

        if (
            last_three[0]
            == last_three[1]
            == last_three[2]
        ):

            return last_three[-1]


    # ---------------------------------
    # Detect alternating pattern
    # ---------------------------------

    if len(player_history) >= 4:

        a = player_history[-4:]
        
        if a[0] == a[2] and a[1] == a[3]:

            return a[-1]


    # ---------------------------------
    # Recent behaviour
    # ---------------------------------

    return most_recent_used


# =========================
# COMPUTER CHOICE
# =========================

def get_computer_choice():

    # =========================
    # LEVEL 1 - EASY
    # =========================

    if difficulty_level == 1:

        return random.choice(choices)


    # =========================
    # LEVEL 2 - NORMAL
    # =========================

    if difficulty_level == 2:

        if len(player_history) < 2:

            return random.choice(choices)


        predicted_move = predict_player_move()


        # 55% prediction
        if random.random() < 0.55:

            return counter[predicted_move]


        return random.choice(choices)


    # =========================
    # LEVEL 3 - HARD
    # =========================

    if difficulty_level == 3:

        if len(player_history) < 2:

            return random.choice(choices)


        predicted_move = predict_player_move()


        # 75% prediction
        if random.random() < 0.75:

            return counter[predicted_move]


        return random.choice(choices)


    # =========================
    # LEVEL 4 - VERY HARD
    # =========================

    if difficulty_level >= 4:

        if len(player_history) < 3:

            return random.choice(choices)


        predicted_move = predict_player_move()


        # 85% prediction
        if random.random() < 0.85:

            return counter[predicted_move]


        return random.choice(choices)


# =========================
# PLAY GAME
# =========================

def play_game(player_choice):

    global player_score
    global computer_score
    global computer_choice


    # Computer chooses BEFORE
    # remembering current move

    computer_choice = get_computer_choice()


    # Remember player's move

    player_history.append(player_choice)


    # =========================
    # DRAW
    # =========================

    if player_choice == computer_choice:

        return "It's a Draw! 🤝"


    # =========================
    # PLAYER WINS
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
    # COMPUTER WINS
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

    player_history = []


    # Difficulty stays the same.
    #
    # Example:
    # Easy → win → Normal
    # Normal → win → Hard
    #
    # Starting a new match does NOT
    # reset the difficulty.


# =========================
# PLAYER WON
# INCREASE DIFFICULTY
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