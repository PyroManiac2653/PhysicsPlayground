import numbers

def format_qotd(number, complexity, genre, hints, question, instructions, attachments):
    str = "QOTD:  #" + number
    return str

def calculate_score(complexity, attempts):
    if not isinstance(complexity, numbers.Number) or complexity < 1 or complexity > 4:
        raise Exception(f"complexity argument is: {complexity}")
    if not isinstance(attempts, numbers.Number) or attempts < 1:
        raise Exception(f"attempts argument is: {attempts}")

    scoring_complexity_attempts = {
        1: { 1: 3, 2: 2, 3: 1, "r": .5 },
        2: { 1: 3.5, 2: 2.5, 3: 1.5, "r": 1 },
        3: { 1: 4.5, 2: 3.5, 3: 2.5, "r": 2 },
        4: { 1: 6, 2: 5, 3: 4, "r": 3.5 }
    }

    if attempts > 3:
        attempts = "r"

    return scoring_complexity_attempts[complexity, attempts]

