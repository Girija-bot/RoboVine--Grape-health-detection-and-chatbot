
def chatbot_response(user_input):
    responses = {
        "how to prevent gray mold": "Ensure good air circulation and avoid overhead watering.",
        "what is powdery mildew": "Powdery mildew is a fungal disease that looks like white powder on leaves.",
        "how to treat black mold": "Use fungicides and improve vineyard hygiene.",
        "how to water grape plants": "Water deeply but infrequently, preferably in the early morning.",
        "what is the best temperature for grape growth": "Grapes grow best in temperatures between 15°C and 30°C."
    }

    # Convert input to lowercase for basic matching
    user_input_lower = user_input.lower()

    # Find the best match
    for key in responses:
        if key in user_input_lower:
            return responses[key]

    return "I'm still learning! Please ask about grape diseases, care, or watering tips."
