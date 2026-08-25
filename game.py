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
# Level 2 = Smart
# Level 3 = Hard
# Level 4 = Master

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
# TRANSITION MEMORY
# =========================

transition_memory = {
    "rock": {
        "rock": 0,
        "paper": 0,
        "scissors": 0
    },

    "paper": {
        "rock": 0,
        "paper": 0,
        "scissors": 0
    },

    "scissors": {
        "rock": 0,
        "paper": 0,
        "scissors": 0
    }
}


# =========================
# UPDATE AI MEMORY
# =========================

def update_memory():

    if len(player_history) < 2:
        return

    previous_move = player_history[-2]
    current_move = player_history[-1]

    transition_memory[previous_move][current_move] += 1


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
# RECENT MOVE PREDICTION
# =========================

def predict_recent():

    if not player_history:
        return random.choice(choices)

    recent = player_history[-7:]

    counts = {
        move: recent.count(move)
        for move in choices
    }

    return max(
        choices,
        key=counts.get
    )


# =========================
# TRANSITION PREDICTION
# =========================

def predict_transition():

    if not player_history:
        return None

    last_move = player_history[-1]

    data = transition_memory[last_move]

    total = sum(data.values())

    if total == 0:
        return None

    return max(
        choices,
        key=lambda move: data[move]
    )


# =========================
# REPEATED MOVE DETECTION
# =========================

def predict_repetition():

    if len(player_history) < 3:
        return None

    last_three = player_history[-3:]

    if (
        last_three[0]
        == last_three[1]
        == last_three[2]
    ):
        return last_three[-1]

    return None


# =========================
# ALTERNATING PATTERN
# =========================

def predict_alternating():

    if len(player_history) < 4:
        return None

    last_four = player_history[-4:]

    if (
        last_four[0] == last_four[2]
        and
        last_four[1] == last_four[3]
    ):
        return last_four[0]

    return None


# =========================
# SEQUENCE DETECTION
# =========================

def predict_sequence():

    if len(player_history) < 6:
        return None

    for length in [3, 2]:

        if len(player_history) <= length:
            continue

        pattern = player_history[-length:]

        possible_next = []

        for i in range(
            len(player_history) - length
        ):

            old_pattern = player_history[
                i:i + length
            ]

            if old_pattern == pattern:

                next_index = i + length

                if next_index < len(player_history):

                    possible_next.append(
                        player_history[next_index]
                    )

        if possible_next:

            return max(
                choices,
                key=possible_next.count
            )

    return None


# =========================
# ADVANCED PREDICTION ENGINE
# =========================

def predict_player_move():

    if not player_history:
        return random.choice(choices)

    predictions = []

    # Recent behaviour
    recent_prediction = predict_recent()

    predictions.append(
        (recent_prediction, 2)
    )

    # Transition behaviour
    transition_prediction = predict_transition()

    if transition_prediction:

        predictions.append(
            (transition_prediction, 4)
        )

    # Repetition
    repetition_prediction = predict_repetition()

    if repetition_prediction:

        predictions.append(
            (repetition_prediction, 5)
        )

    # Alternating pattern
    alternating_prediction = predict_alternating()

    if alternating_prediction:

        predictions.append(
            (alternating_prediction, 5)
        )

    # Sequence prediction
    sequence_prediction = predict_sequence()

    if sequence_prediction:

        predictions.append(
            (sequence_prediction, 6)
        )

    # =========================
    # SCORE PREDICTIONS
    # =========================

    scores = {
        "rock": 0,
        "paper": 0,
        "scissors": 0
    }

    for prediction, weight in predictions:

        scores[prediction] += weight

    return max(
        choices,
        key=lambda move: scores[move]
    )


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
    # LEVEL 2 - SMART
    # =========================

    if difficulty_level == 2:

        if len(player_history) < 2:

            return random.choice(choices)

        predicted = predict_player_move()

        # 70% prediction
        if random.random() < 0.70:

            return counter[predicted]

        return random.choice(choices)


    # =========================
    # LEVEL 3 - HARD
    # =========================

    if difficulty_level == 3:

        if len(player_history) < 3:

            return random.choice(choices)

        predicted = predict_player_move()

        # 88% prediction
        if random.random() < 0.88:

            return counter[predicted]

        return random.choice(choices)


    # =========================
    # LEVEL 4 - MASTER
    # =========================

    if difficulty_level >= 4:

        if len(player_history) < 4:

            return random.choice(choices)

        predicted = predict_player_move()

        # 97% prediction
        if random.random() < 0.97:

            return counter[predicted]

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

    player_history.append(
        player_choice
    )

    update_memory()

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
    global transition_memory

    player_score = 0
    computer_score = 0
    computer_choice = ""

    player_history = []

    # Reset AI memory

    transition_memory = {
        "rock": {
            "rock": 0,
            "paper": 0,
            "scissors": 0
        },

        "paper": {
            "rock": 0,
            "paper": 0,
            "scissors": 0
        },

        "scissors": {
            "rock": 0,
            "paper": 0,
            "scissors": 0
        }
    }


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