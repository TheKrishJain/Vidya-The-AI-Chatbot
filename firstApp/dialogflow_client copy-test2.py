from google.cloud import dialogflow_v2 as dialogflow

import os

# Set Google Credentials (Replace with your JSON key path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/msi/Desktop/Ai-Chatbot-main/Chatbot_using_Django/aiChatBot/firstApp/charged-kiln-445717-k7-0f017d9755cf.json"

# Dialogflow Project ID
PROJECT_ID = "charged-kiln-445717-k7"  # Replace with your project ID
SESSION_ID = "test-session"  # A random session ID (can be any unique string)


def detect_intent_texts(project_id, session_id, texts, language_code="en"):
    """Sends user input to Dialogflow and returns the response."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)

        print(f"/nUser: {text}")
        print(f"Bot: {response.query_result.fulfillment_text}")


# Sample test questions
sample_questions = [
    "Hello!",
    "What services do you provide?",
    "Tell me a joke.",
    "How can I contact support?",
]

# Run the test
detect_intent_texts(PROJECT_ID, SESSION_ID, sample_questions)
