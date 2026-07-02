def latest_user_message(messages):
    """
    Returns the latest user message.
    """

    for msg in reversed(messages):
        if msg["role"] == "user":
            return msg["content"].lower()

    return ""


def previous_messages(messages):
    """
    Returns previous conversation as text.
    """

    history = []

    for msg in messages:
        history.append(msg["content"])

    return " ".join(history).lower()