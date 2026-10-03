import json


# ============================================================
# 1. LOAD QUESTION BANK
# ============================================================

with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

questions = data["questions"]


# ============================================================
# 2. FIND A QUESTION
# ============================================================

def get_question(question_id):
    """
    Find a question using its question_id.
    """

    for question in questions:
        if question["question_id"] == question_id:
            return question

    return None


# ============================================================
# 3. CALCULATE METRICS
# ============================================================

def calculate_metrics(clicks, hits, misses):
    """
    Calculate the six ML features.
    """

    if clicks > 0:
        accuracy = hits / clicks
        missrate = misses / clicks
    else:
        accuracy = 0
        missrate = 0

    score = hits

    return {
        "clicks": clicks,
        "hits": hits,
        "misses": misses,
        "score": score,
        "accuracy": accuracy,
        "missrate": missrate
    }


# ============================================================
# 4. CLICK QUESTION
# ============================================================

def validate_click_question(question_id, attempts):
    """
    Validate click-based questions.

    Example:
    attempts = ["D", "P", "B"]
    correct answer = "B"
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    correct_answer = question.get("correct_answer")

    clicks = len(attempts)
    hits = 0
    misses = 0

    for answer in attempts:

        if answer == correct_answer:
            hits += 1
        else:
            misses += 1

    return calculate_metrics(clicks, hits, misses)


# ============================================================
# 5. ARRANGE QUESTION
# ============================================================

def validate_arrange_question(question_id, final_order):
    """
    Validate drag-and-drop / arrangement questions.

    Used for Q21 and Q22.
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    correct_order = question.get("correct_order")

    clicks = len(final_order)

    if final_order == correct_order:
        hits = clicks
        misses = 0
    else:
        hits = 0
        misses = clicks

    return calculate_metrics(clicks, hits, misses)


# ============================================================
# 6. SEQUENCE / MEMORY QUESTION
# ============================================================

def validate_sequence_question(question_id, submitted_sequence):
    """
    Validate memory and sequence questions.

    Used for Q23, Q24, Q26 and Q28.
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    correct_sequence = question.get("sequence")

    clicks = len(submitted_sequence)
    hits = 0
    misses = 0

    # Compare each position
    for i in range(min(len(submitted_sequence), len(correct_sequence))):

        if submitted_sequence[i] == correct_sequence[i]:
            hits += 1
        else:
            misses += 1

    # Extra/missing items count as misses
    if len(submitted_sequence) > len(correct_sequence):
        misses += len(submitted_sequence) - len(correct_sequence)

    if len(submitted_sequence) < len(correct_sequence):
        misses += len(correct_sequence) - len(submitted_sequence)

    return calculate_metrics(clicks, hits, misses)


# ============================================================
# 7. AUDITORY SEQUENCE QUESTION
# ============================================================

def validate_audio_question(question_id, submitted_sequence):
    """
    Validate auditory working-memory question.

    Used for Q32.
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    correct_sequence = question.get("correct_sequence")

    clicks = len(submitted_sequence)
    hits = 0
    misses = 0

    for i in range(min(len(submitted_sequence), len(correct_sequence))):

        if submitted_sequence[i] == correct_sequence[i]:
            hits += 1
        else:
            misses += 1

    if len(submitted_sequence) > len(correct_sequence):
        misses += len(submitted_sequence) - len(correct_sequence)

    if len(submitted_sequence) < len(correct_sequence):
        misses += len(correct_sequence) - len(submitted_sequence)

    return calculate_metrics(clicks, hits, misses)


# ============================================================
# 8. ACADEMIC SELF-REPORT QUESTIONS
# ============================================================

def validate_self_report(question_id, selected_option):
    """
    Validate academic-effect questions.

    These questions do NOT have right/wrong answers.

    Used for Q29, Q30 and Q31.
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    return {
        "question_id": question_id,
        "response": selected_option,
        "response_type": "self_report",
        "valid": True
    }


# ============================================================
# 9. PROCESS ANY QUESTION AUTOMATICALLY
# ============================================================

def process_question(question_id, response):
    """
    Automatically choose the correct validation method
    according to the question's interaction type.
    """

    question = get_question(question_id)

    if question is None:
        return {"error": "Question not found"}

    interaction_type = question.get("interaction_type")

    # --------------------------------------------
    # CLICK QUESTIONS
    # --------------------------------------------

    if interaction_type == "click":

        # Academic questions are self-report
        if question.get("response_type") == "self_report":
            return validate_self_report(
                question_id,
                response
            )

        return validate_click_question(
            question_id,
            response
        )

    # --------------------------------------------
    # ARRANGE QUESTIONS
    # --------------------------------------------

    elif interaction_type == "arrange":

        return validate_arrange_question(
            question_id,
            response
        )

    # --------------------------------------------
    # MEMORY / SEQUENCE QUESTIONS
    # --------------------------------------------

    elif interaction_type == "sequence":

        return validate_sequence_question(
            question_id,
            response
        )

    # --------------------------------------------
    # AUDITORY MEMORY
    # --------------------------------------------

    elif interaction_type == "listen_and_sequence":

        return validate_audio_question(
            question_id,
            response
        )

    else:

        return {
            "error": "Unknown interaction type",
            "interaction_type": interaction_type
        }


# ============================================================
# 10. TEST ALL 32 QUESTIONS
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("DYSLEXIA QUESTION VALIDATION TEST")
    print("========================================\n")


    # --------------------------------------------------------
    # Q1 - CLICK
    # --------------------------------------------------------

    print("Q1")

    result = process_question(
        1,
        ["D", "P", "B"]
    )

    print(result)


    # --------------------------------------------------------
    # Q2 - CLICK
    # --------------------------------------------------------

    print("\nQ2")

    result = process_question(
        2,
        ["N", "M"]
    )

    print(result)


    # --------------------------------------------------------
    # Q3 - CLICK
    # --------------------------------------------------------

    print("\nQ3")

    result = process_question(
        3,
        ["q", "p"]
    )

    print(result)


    # --------------------------------------------------------
    # Q4 - CLICK
    # --------------------------------------------------------

    print("\nQ4")

    result = process_question(
        4,
        ["T", "S"]
    )

    print(result)


    # --------------------------------------------------------
    # Q5 - CLICK
    # --------------------------------------------------------

    print("\nQ5")

    result = process_question(
        5,
        ["rabbit", "tiger"]
    )

    print(result)


    # --------------------------------------------------------
    # Q6 - CLICK
    # --------------------------------------------------------

    print("\nQ6")

    result = process_question(
        6,
        ["book", "bike"]
    )

    print(result)


    # --------------------------------------------------------
    # Q7 - CLICK
    # --------------------------------------------------------

    print("\nQ7")

    result = process_question(
        7,
        ["rabbit", "marker"]
    )

    print(result)


    # --------------------------------------------------------
    # Q8 - CLICK
    # --------------------------------------------------------

    print("\nQ8")

    result = process_question(
        8,
        ["sit", "night"]
    )

    print(result)


    # --------------------------------------------------------
    # Q9 - CLICK
    # --------------------------------------------------------

    print("\nQ9")

    result = process_question(
        9,
        ["ring", "train"]
    )

    print(result)


    # --------------------------------------------------------
    # Q10 - CLICK
    # --------------------------------------------------------

    print("\nQ10")

    result = process_question(
        10,
        ["scool", "school"]
    )

    print(result)


    # --------------------------------------------------------
    # Q11 - CLICK
    # --------------------------------------------------------

    print("\nQ11")

    result = process_question(
        11,
        ["blick", "garden"]
    )

    print(result)


    # --------------------------------------------------------
    # Q12 - CLICK
    # --------------------------------------------------------

    print("\nQ12")

    result = process_question(
        12,
        ["cat", "dog"]
    )

    print(result)


    # --------------------------------------------------------
    # Q13 - CLICK
    # --------------------------------------------------------

    print("\nQ13")

    result = process_question(
        13,
        ["becouse", "because"]
    )

    print(result)


    # --------------------------------------------------------
    # Q14 - CLICK
    # --------------------------------------------------------

    print("\nQ14")

    result = process_question(
        14,
        ["X", "K"]
    )

    print(result)


    # --------------------------------------------------------
    # Q15 - CLICK
    # --------------------------------------------------------

    print("\nQ15")

    result = process_question(
        15,
        ["C", "G"]
    )

    print(result)


    # --------------------------------------------------------
    # Q16 - CLICK
    # --------------------------------------------------------

    print("\nQ16")

    result = process_question(
        16,
        ["son", "sun"]
    )

    print(result)


    # --------------------------------------------------------
    # Q17 - CLICK
    # --------------------------------------------------------

    print("\nQ17")

    result = process_question(
        17,
        ["freind", "friend"]
    )

    print(result)


    # --------------------------------------------------------
    # Q18 - CLICK
    # --------------------------------------------------------

    print("\nQ18")

    result = process_question(
        18,
        ["becaus", "because"]
    )

    print(result)


    # --------------------------------------------------------
    # Q19 - CLICK
    # --------------------------------------------------------

    print("\nQ19")

    result = process_question(
        19,
        ["T", "S"]
    )

    print(result)


    # --------------------------------------------------------
    # Q20 - CLICK
    # --------------------------------------------------------

    print("\nQ20")

    result = process_question(
        20,
        ["A (first)", "A (second)"]
    )

    print(result)


    # --------------------------------------------------------
    # Q21 - ARRANGE
    # --------------------------------------------------------

    print("\nQ21")

    result = process_question(
        21,
        ["C", "A", "T"]
    )

    print(result)


    # --------------------------------------------------------
    # Q22 - ARRANGE
    # --------------------------------------------------------

    print("\nQ22")

    result = process_question(
        22,
        ["I", "LIKE", "READING"]
    )

    print(result)


    # --------------------------------------------------------
    # Q23 - MEMORY
    # --------------------------------------------------------

    print("\nQ23")

    result = process_question(
        23,
        ["red", "blue", "green"]
    )

    print(result)


    # --------------------------------------------------------
    # Q24 - MEMORY
    # --------------------------------------------------------

    print("\nQ24")

    result = process_question(
        24,
        ["star", "circle", "square"]
    )

    print(result)


    # --------------------------------------------------------
    # Q25 - PROCESSING SPEED
    # --------------------------------------------------------

    print("\nQ25")

    result = process_question(
        25,
        ["N", "M"]
    )

    print(result)


    # --------------------------------------------------------
    # Q26 - MEMORY
    # --------------------------------------------------------

    print("\nQ26")

    result = process_question(
        26,
        ["4", "B", "9"]
    )

    print(result)


    # --------------------------------------------------------
    # Q27 - PROCESSING SPEED
    # --------------------------------------------------------

    print("\nQ27")

    result = process_question(
        27,
        ["R", "P"]
    )

    print(result)


    # --------------------------------------------------------
    # Q28 - SEQUENCE
    # --------------------------------------------------------

    print("\nQ28")

    result = process_question(
        28,
        ["A", "5", "C", "2"]
    )

    print(result)


    # --------------------------------------------------------
    # Q29 - ACADEMIC SELF REPORT
    # --------------------------------------------------------

    print("\nQ29")

    result = process_question(
        29,
        "Often"
    )

    print(result)


    # --------------------------------------------------------
    # Q30 - ACADEMIC SELF REPORT
    # --------------------------------------------------------

    print("\nQ30")

    result = process_question(
        30,
        "Sometimes"
    )

    print(result)


    # --------------------------------------------------------
    # Q31 - ACADEMIC SELF REPORT
    # --------------------------------------------------------

    print("\nQ31")

    result = process_question(
        31,
        "Often"
    )

    print(result)


    # --------------------------------------------------------
    # Q32 - AUDITORY MEMORY
    # --------------------------------------------------------

    print("\nQ32")

    result = process_question(
        32,
        ["B", "7", "K"]
    )

    print(result)


    print("\n========================================")
    print("ALL 32 QUESTIONS TESTED")
    print("========================================")