def calculate_score(
    correct,
    total
):

    if total == 0:
        return 0

    return round(
        (correct / total) * 100,
        2
    )


def performance_level(score):

    if score >= 80:
        return "Strong"

    elif score >= 50:
        return "Average"

    return "Needs Revision"


def get_recommendation(score):

    if score >= 80:

        return (
            "Excellent! Keep practicing "
            "and move to advanced topics."
        )

    elif score >= 50:

        return (
            "Good progress. Revise your notes "
            "and practice more questions."
        )

    return (
        "This topic needs revision. "
        "Review your notes and retake the quiz."
    )


def find_weak_topics(
    quiz_data,
    user_answers
):

    weak_topics = []

    for index, question in enumerate(
        quiz_data
    ):

        if (
            user_answers.get(index)
            != question.get("answer")
        ):

            topic = question.get(
                "topic",
                "General"
            )

            if topic not in weak_topics:

                weak_topics.append(
                    topic
                )

    return weak_topics