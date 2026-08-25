import random


# =========================================================
# GAME SETTINGS
# =========================================================

choices = ["rock", "paper", "scissors"]

player_score = 0
computer_score = 0
computer_choice = ""

player_history = []

WINNING_SCORE = 10


# =========================================================
# DIFFICULTY
# =========================================================

# All levels are strong.
#
# Level 1 = Beginner AI
# Level 2 = Advanced AI
# Level 3 = Expert AI
# Level 4 = Master AI

difficulty_level = 1


# =========================================================
# COUNTER MOVES
# =========================================================

counter = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}


# =========================================================
# AI MEMORY
# =========================================================

# Learns what the player does after another move.

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


# =========================================================
# TWO-MOVE MEMORY
# =========================================================

# Learns patterns such as:
#
# rock, paper -> scissors
# paper, rock -> paper

pair_memory = {}


# =========================================================
# THREE-MOVE MEMORY
# =========================================================

# Learns longer patterns.

triple_memory = {}


# =========================================================
# STRATEGY LEARNING
# =========================================================

strategy_score = {
    "recent": 1.0,
    "frequency": 1.0,
    "transition": 1.0,
    "repeat": 1.0,
    "alternate": 1.0,
    "sequence2": 1.0,
    "sequence3": 1.0
}


# =========================================================
# LAST PREDICTIONS
# =========================================================

last_predictions = {}


# =========================================================
# AI CONFIDENCE
# =========================================================

ai_confidence = 0.0


# =========================================================
# UPDATE TRANSITION MEMORY
# =========================================================

def update_transition_memory():

    if len(player_history) < 2:
        return

    previous_move = player_history[-2]
    current_move = player_history[-1]

    transition_memory[
        previous_move
    ][current_move] += 1


# =========================================================
# UPDATE PAIR MEMORY
# =========================================================

def update_pair_memory():

    if len(player_history) < 3:
        return

    pair = tuple(player_history[-3:-1])
    next_move = player_history[-1]

    if pair not in pair_memory:

        pair_memory[pair] = {
            "rock": 0,
            "paper": 0,
            "scissors": 0
        }

    pair_memory[pair][next_move] += 1


# =========================================================
# UPDATE TRIPLE MEMORY
# =========================================================

def update_triple_memory():

    if len(player_history) < 4:
        return

    triple = tuple(player_history[-4:-1])
    next_move = player_history[-1]

    if triple not in triple_memory:

        triple_memory[triple] = {
            "rock": 0,
            "paper": 0,
            "scissors": 0
        }

    triple_memory[triple][next_move] += 1


# =========================================================
# UPDATE ALL MEMORY
# =========================================================

def update_memory():

    update_transition_memory()
    update_pair_memory()
    update_triple_memory()


# =========================================================
# FREQUENCY PREDICTION
# =========================================================

def predict_frequency():

    if not player_history:
        return random.choice(choices)

    counts = {
        move: player_history.count(move)
        for move in choices
    }

    return max(
        choices,
        key=counts.get
    )


# =========================================================
# RECENT PREDICTION
# =========================================================

def predict_recent():

    if not player_history:
        return random.choice(choices)

    recent = player_history[-8:]

    counts = {
        move: recent.count(move)
        for move in choices
    }

    return max(
        choices,
        key=counts.get
    )


# =========================================================
# TRANSITION PREDICTION
# =========================================================

def predict_transition():

    if not player_history:
        return None

    last_move = player_history[-1]

    data = transition_memory[last_move]

    if sum(data.values()) == 0:
        return None

    return max(
        choices,
        key=lambda move: data[move]
    )


# =========================================================
# REPEATED MOVE PREDICTION
# =========================================================

def predict_repeat():

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


# =========================================================
# ALTERNATING PATTERN
# =========================================================

def predict_alternate():

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


# =========================================================
# TWO-MOVE PATTERN
# =========================================================

def predict_sequence2():

    if len(player_history) < 3:
        return None

    pattern = tuple(player_history[-2:])

    if pattern not in pair_memory:
        return None

    data = pair_memory[pattern]

    if sum(data.values()) == 0:
        return None

    return max(
        choices,
        key=lambda move: data[move]
    )


# =========================================================
# THREE-MOVE PATTERN
# =========================================================

def predict_sequence3():

    if len(player_history) < 4:
        return None

    pattern = tuple(player_history[-3:])

    if pattern not in triple_memory:
        return None

    data = triple_memory[pattern]

    if sum(data.values()) == 0:
        return None

    return max(
        choices,
        key=lambda move: data[move]
    )


# =========================================================
# LEARN WHICH PREDICTOR IS WORKING
# =========================================================

def learn_from_previous_round():

    if len(player_history) < 1:
        return

    actual_move = player_history[-1]

    for strategy, prediction in last_predictions.items():

        if prediction is None:
            continue

        if prediction == actual_move:

            # Correct prediction gets stronger.

            strategy_score[strategy] += 2.0

        else:

            # Wrong prediction becomes weaker.

            strategy_score[strategy] *= 0.88


    # Keep values under control.

    for strategy in strategy_score:

        if strategy_score[strategy] < 0.15:

            strategy_score[strategy] = 0.15

        if strategy_score[strategy] > 100:

            strategy_score[strategy] = 100


# =========================================================
# SELF-LEARNING PREDICTION ENGINE
# =========================================================

def predict_player_move():

    global ai_confidence

    if not player_history:

        ai_confidence = 0

        return random.choice(choices)


    predictions = {

        "recent": predict_recent(),

        "frequency": predict_frequency(),

        "transition": predict_transition(),

        "repeat": predict_repeat(),

        "alternate": predict_alternate(),

        "sequence2": predict_sequence2(),

        "sequence3": predict_sequence3()
    }


    # -----------------------------------------------------
    # Give every predicted move a learned score.
    # -----------------------------------------------------

    move_scores = {
        "rock": 0.0,
        "paper": 0.0,
        "scissors": 0.0
    }


    total_weight = 0

    for strategy, prediction in predictions.items():

        if prediction is None:
            continue

        weight = strategy_score[strategy]

        move_scores[prediction] += weight

        total_weight += weight


    # -----------------------------------------------------
    # If there is no useful prediction.
    # -----------------------------------------------------

    if total_weight == 0:

        ai_confidence = 0

        return random.choice(choices)


    # -----------------------------------------------------
    # Find strongest prediction.
    # -----------------------------------------------------

    best_move = max(
        choices,
        key=lambda move: move_scores[move]
    )


    # -----------------------------------------------------
    # Calculate confidence.
    # -----------------------------------------------------

    strongest = move_scores[best_move]

    second_best = sorted(
        move_scores.values(),
        reverse=True
    )[1]

    difference = strongest - second_best

    ai_confidence = (
        difference / total_weight
    )


    # Save predictions for learning.

    global last_predictions

    last_predictions = predictions.copy()


    return best_move


# =========================================================
# ADAPTIVE RANDOMNESS
# =========================================================

def get_prediction_strength():

    # The AI becomes stronger as it gets
    # more information about the player.

    history_length = len(player_history)


    if history_length < 3:
        return 0.60


    if history_length < 5:
        return 0.72


    if history_length < 8:
        return 0.82


    if history_length < 12:
        return 0.90


    return 0.95


# =========================================================
# COMPUTER CHOICE
# =========================================================

def get_computer_choice():

    # -----------------------------------------------------
    # Not enough information yet.
    # -----------------------------------------------------

    if len(player_history) < 2:

        return random.choice(choices)


    predicted_move = predict_player_move()

    prediction_strength = get_prediction_strength()


    # =====================================================
    # LEVEL 1 - STRONG
    # =====================================================

    if difficulty_level == 1:

        strength = max(
            0.65,
            prediction_strength - 0.08
        )

        if random.random() < strength:

            return counter[predicted_move]

        return random.choice(choices)


    # =====================================================
    # LEVEL 2 - VERY STRONG
    # =====================================================

    if difficulty_level == 2:

        strength = max(
            0.72,
            prediction_strength
        )

        if random.random() < strength:

            return counter[predicted_move]

        return random.choice(choices)


    # =====================================================
    # LEVEL 3 - EXPERT
    # =====================================================

    if difficulty_level == 3:

        strength = max(
            0.82,
            prediction_strength + 0.03
        )

        if random.random() < strength:

            return counter[predicted_move]

        return random.choice(choices)


    # =====================================================
    # LEVEL 4 - MASTER
    # =====================================================

    if difficulty_level >= 4:

        strength = max(
            0.90,
            prediction_strength + 0.05
        )

        if random.random() < strength:

            return counter[predicted_move]

        return random.choice(choices)


# =========================================================
# PLAY GAME
# =========================================================

def play_game(player_choice):

    global player_score
    global computer_score
    global computer_choice


    # =====================================================
    # LEARN FROM THE PREVIOUS ROUND
    # =====================================================

    learn_from_previous_round()


    # =====================================================
    # COMPUTER THINKS
    # =====================================================

    computer_choice = get_computer_choice()


    # =====================================================
    # REMEMBER CURRENT PLAYER MOVE
    # =====================================================

    player_history.append(player_choice)

    update_memory()


    # =====================================================
    # DRAW
    # =====================================================

    if player_choice == computer_choice:

        return "It's a Draw! 🤝"


    # =====================================================
    # PLAYER WINS
    # =====================================================

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


    # =====================================================
    # COMPUTER WINS
    # =====================================================

    computer_score += 1


    if computer_score >= WINNING_SCORE:

        return "🤖 COMPUTER IS THE CHAMPION!"


    return "You Lose! 😢"


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global player_score
    global computer_score
    global computer_choice
    global player_history
    global transition_memory
    global pair_memory
    global triple_memory
    global strategy_score
    global last_predictions
    global ai_confidence


    player_score = 0
    computer_score = 0
    computer_choice = ""

    player_history = []


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


    pair_memory = {}

    triple_memory = {}


    strategy_score = {
        "recent": 1.0,
        "frequency": 1.0,
        "transition": 1.0,
        "repeat": 1.0,
        "alternate": 1.0,
        "sequence2": 1.0,
        "sequence3": 1.0
    }


    last_predictions = {}

    ai_confidence = 0.0


# =========================================================
# PLAYER WON
# =========================================================

def player_won():

    global difficulty_level

    if difficulty_level < 4:

        difficulty_level += 1


# =========================================================
# GET DIFFICULTY
# =========================================================

def get_difficulty():

    return difficulty_level