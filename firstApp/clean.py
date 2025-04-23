from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# Set credentials explicitly (for testing)
credentials = service_account.Credentials.from_service_account_file("firstApp/prime-force-445815-c4-a3f9bb3ae3c1.json")
project_id = "prime-force-445815-c4"
session_id = "test-session"

def test_dialogflow():
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.TextInput(text="Hello", language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        print("Dialogflow Response:", response.query_result.fulfillment_text)
    except Exception as e:
        print("Dialogflow Error:", e)

test_dialogflow()