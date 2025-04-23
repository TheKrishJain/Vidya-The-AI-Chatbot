import json
import os
import time  # Import the time module
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .new import get_response, send_name_to_dialogflow # Import the function from new.py
from django.core.mail import send_mail
import django.core.mail
from .models import UserInfo
from .models import ChatMessage
from django.utils import timezone
import json
import random
from django.http import JsonResponse

import json
from django.http import JsonResponse


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




# @csrf_exempt

# def normalize_course(course_raw):
#     return course_raw.lower().replace(" ", "").replace(".", "")

# def calculate_eligibility(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request method"}, status=405)

#     try:
#         data = json.loads(request.body)
#         parameters = data.get("queryResult", {}).get("parameters", {})

#         # Normalize input
#         course = normalize_course(parameters.get("course", ""))
#         percentage = parameters.get("percentage", 0)
#         stream = parameters.get("stream", "").lower()
#         reserved = parameters.get("reserved", "").lower()

#         # Check for missing parameters
#         missing_parameters = []
#         if not course: missing_parameters.append("course")
#         if not percentage: missing_parameters.append("percentage")
#         if not stream: missing_parameters.append("stream")
#         if not reserved: missing_parameters.append("reserved")

#         if missing_parameters:
#             prompts = {
#                 "course": "Which course are you interested in? (e.g., B.Sc. IT, M.Com, MA)",
#                 "percentage": "Please let me know your 12th percentage.",
#                 "stream": "Please let me know your stream (e.g., Science, Commerce, Arts).",
#                 "reserved": "Are you from a reserved category? (Yes/No)"
#             }
#             return JsonResponse({"fulfillmentText": prompts[missing_parameters[0]]})

#         # Eligibility checking
#         eligibility = False
#         message = ""

#         # Mapping multiple variants of the same course
#         course_map = {
#             "bscit": ["bscit", "bscinformationtechnology", "bscit"],
#             "bscds": ["bscds", "bscdatascience"],
#             "bms": ["bms"],
#             "bcom": ["bcom", "bcomaccountingfinance", "bcombankinginsurance", "bcomgeneral", "bfm"],
#             "ba": ["ba", "bamasscommunication", "bamultimedia", "bachelorofarts"],
#             "msc": ["mscit", "msc", "msc.it", "masterofscienceit"],
#             "mcom": ["mcom", "masterofcommerce"],
#             "ma": ["ma", "masterofarts"]
#         }

#         matched_course = None
#         for key, aliases in course_map.items():
#             if course in aliases:
#                 matched_course = key
#                 break

#         # Rules for eligibility
#         if matched_course == "bscit":
#             if stream == "science" and ((reserved == "no" and percentage >= 45) or (reserved == "yes" and percentage >= 40)):
#                 eligibility = True
#                 message = "You are eligible for B.Sc. IT. 🎉"
#             else:
#                 message = "You need to have a Science stream with Mathematics to be eligible for B.Sc. IT."

#         elif matched_course == "bscds":
#             if stream == "science" and ((reserved == "no" and percentage >= 45) or (reserved == "yes" and percentage >= 40)):
#                 eligibility = True
#                 message = "You are eligible for B.Sc. Data Science. 🎉"
#             else:
#                 message = "You need to have a Science stream with Mathematics to be eligible for B.Sc. Data Science."

#         elif matched_course == "bms":
#             if (reserved == "no" and percentage >= 45) or (reserved == "yes" and percentage >= 40):
#                 eligibility = True
#                 message = "You are eligible for B.M.S. 🎉"

#         elif matched_course == "bcom":
#             if (reserved == "no" and percentage >= 45) or (reserved == "yes" and percentage >= 40):
#                 eligibility = True
#                 message = "You are eligible for B.Com / B.F.M. 🎉"

#         elif matched_course == "ba":
#             if stream in ["science", "commerce", "arts"]:
#                 eligibility = True
#                 message = "You are eligible for B.A. 🎉"
#             else:
#                 message = "Only Science, Commerce, or Arts stream students are eligible for B.A."

#         elif matched_course == "msc":
#             if percentage >= 50:
#                 eligibility = True
#                 message = "You are eligible for M.Sc. IT. 🎉"
#             else:
#                 message = "You need at least 50% in your graduation to be eligible for M.Sc. IT."

#         elif matched_course == "mcom":
#             if percentage >= 50:
#                 eligibility = True
#                 message = "You are eligible for M.Com. 🎉"
#             else:
#                 message = "You need at least 50% in your graduation to be eligible for M.Com."

#         elif matched_course == "ma":
#             if percentage >= 50:
#                 eligibility = True
#                 message = "You are eligible for M.A. 🎉"
#             else:
#                 message = "You need at least 50% in your graduation to be eligible for M.A."

#         else:
#             message = "Course not recognized. Please enter a valid course name like B.Sc. IT, M.Com, or MA."

#         if not eligibility and "eligible" not in message:
#             message = "You are not eligible for the selected course."

#         return JsonResponse({"fulfillmentText": message})

#     except Exception as e:
#         print(f"Error processing request: {e}")
#         return JsonResponse({"error": "An error occurred while processing the request"}, status=500)






# Render your main HTML template
def index(request):
    return render(request, "index.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
  
            data = json.loads(request.body)
            # Check if the request is for eligibility calculation
            intent = data.get("queryResult", {}).get("intent", {}).get("displayName", "")
         

            message = data.get('message', '')
            language = data.get('language', 'en')  # Get the language from the request
            print(f"Received message: {message}")
             # Capture the time when the message is received
            message_received_time = timezone.now()

            print(f"Message received at: {message_received_time}")
            reply = get_response(message,language)
            
            print(f"Generated reply: {reply}")
            

            if reply is None or reply == "":
                reply = "I'm sorry, I didn't understand that. Can you please rephrase?"

            # Capture the time when the reply is generated
            reply_generated_time = timezone.now()
            print(f"Reply generated at: {reply_generated_time}")   
            chat_message = ChatMessage(
            message=message,
            reply=reply,
            received_time=message_received_time,
            reply_time=reply_generated_time
            )
            chat_message.save()
            response_data = {
                'reply': reply
            }
            return JsonResponse({'response': reply})  # Ensure the key is 'response'
        except json.JSONDecodeError:
            print("Error: Invalid JSON received.")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)





# Render your main HTML template
def index(request):
    return render(request, "index.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
  
            data = json.loads(request.body)
            
            message = data.get('message', '')
            language = data.get('language', 'en')  # Get the language from the request
            print(f"Received message: {message}")
             # Capture the time when the message is received
            message_received_time = timezone.now()

            print(f"Message received at: {message_received_time}")
            reply = get_response(message,language)
            
            print(f"Generated reply: {reply}")
            

            if reply is None or reply == "":
                reply = "I'm sorry, I didn't understand that. Can you please rephrase?"

            # Capture the time when the reply is generated
            reply_generated_time = timezone.now()
            print(f"Reply generated at: {reply_generated_time}")   
            chat_message = ChatMessage(
            message=message,
            reply=reply,
            received_time=message_received_time,
            reply_time=reply_generated_time
            )
            chat_message.save()
            response_data = {
                'reply': reply
            }
            return JsonResponse({'response': reply})  # Ensure the key is 'response'
        except json.JSONDecodeError:
            print("Error: Invalid JSON received.")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def send_user_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('firstName')
            email = data.get('email')
            phone = data.get('phone')
        

            # Process or save the data here
            print(f"Received user info: Name={first_name}, Email={email}, Phone={phone}")

             # Generate personalized greetings in multiple languages
            greetings = [
                f"Namaste {first_name}. How can I help you today?",
                f"Hola {first_name}. How can I help you today?",
                f"Hello {first_name}. How can I help you today?",
                f"Bonjour {first_name}. How can I help you today?",
            ]

            # Select one random greeting
            random_greeting = random.choice(greetings)
            print(f"Selected greeting: {random_greeting}")

            # Capture the time when the reply is generated
            reply_generated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"Reply generated at: {reply_generated_time}")

            # Save user information to the database
            user_info = UserInfo(
                first_name=first_name,
                email=email,
                phone=phone
            )
            user_info.save()

            # Respond with success and the random greeting
            response_data = {
                'message': 'User information saved successfully',
                'greeting': random_greeting,  # Return a single random greeting
                'reply_generated_time': reply_generated_time,
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'message': 'Error processing data'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

# Path to your responses.json file
responses_file_path = os.path.join(os.path.dirname(__file__), 'information/responses.json')

# Load the responses from the JSON file
with open(responses_file_path, 'r') as file:
    responses = json.load(file)

def determine_intent(message):
    # First, check for common intents
    print(f"Determining intent for message: {message}")  # Log the message for intent determination
    if any(keyword in message for keyword in ["hello", "hi", "hey"]):
        print("Intent recognized: greeting")  # Log recognized intent
        return "greeting"
    elif any(keyword in message for keyword in ["goodbye", "bye", "see you later"]):
        print("Intent recognized: goodbye")  # Log recognized intent
        return "goodbye"
    elif any(keyword in message for keyword in ["thanks", "thank you"]):
        print("Intent recognized: thanks")  # Log recognized intent
        return "thanks"
    elif any(keyword in message for keyword in ["help", "what can you do"]):
        print("Intent recognized: help")  # Log recognized intent
        return "help"
    
    # If no common intent is found, check the questions from questions.json
    try:
        questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
        with open(questions_file_path, 'r') as file:
            data = json.load(file)
            questions = data['questions']

            # Perform a more robust search for the matching question
            for question in questions:
                print(f"Checking question: {question['text']}")  # Log the question being checked
                if question['text'].lower() in message or message in question['text'].lower():
                    print(f"Intent matched: question_match, answer: {question['answer']}")  # Log matched question and answer
                    return {'intent': 'question_match', 'answer': question['answer']}
    except FileNotFoundError:
        print("Questions file not found")  # Log file not found error

    return None  # If no match is found, return None

@csrf_exempt
def suggested_questions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load JSON data
            query = data.get('query', '').lower()  # Get the query
            print(f"Received query for suggestions: {query}")  # Log received query

            with open('firstApp/questions.json', 'r') as file:
                data = json.load(file)
                questions = data['questions']

                # Filter questions based on query using more efficient matching
                filtered_questions = [
                    question for question in questions 
                    if query in question['text'].lower()  # Simple containment check
                    or question['text'].lower().startswith(query)  # Start with query
                ][:5]  # Limit suggestions to top 5

                print(f"Filtered questions: {filtered_questions}")  # Log filtered questions
                response_data = {
                    'questions': filtered_questions
                }
                return JsonResponse(response_data)  # Return the filtered questions
        except json.JSONDecodeError:
            print("Error: Invalid JSON received for suggested questions.")  # Log JSON decode error
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def answer(request, question_id):
    if request.method == 'GET':
        try:
            with open('firstApp/questions.json', 'r') as file:
                data = json.load(file)
                questions = data['questions']

                # Find the question by ID
                question = next((q for q in questions if q['id'] == question_id), None)
                if question:
                    print(f"Found question ID: {question_id}, answer: {question['answer']}")  # Log found question and answer
                    response_data = {
                        'answer': question['answer']  # Assuming your questions JSON has an 'answer' field
                    }
                    return JsonResponse(response_data)
                else:
                    print(f"Question ID: {question_id} not found.")  # Log question not found
                    return JsonResponse({'error': 'Question not found'}, status=404)
        except json.JSONDecodeError:
            print("Error: Invalid JSON received when fetching answer.")  # Log JSON decode error
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except FileNotFoundError:
            print("Questions file not found when fetching answer.")  # Log file not found error
            return JsonResponse({'error': 'Questions file not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)








################################################################################################33
import logging
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def send_transcript(request):
    logger.info(f"Received request method: {request.method}")

    if request.method == 'POST':
        try:
            # Parse the incoming request body

            data = json.loads(request.body)
            
            email = data.get('email')
            transcript = data.get('transcript')

            if not email or not transcript:
                logger.error("Missing email or transcript.")
                return JsonResponse({'error': 'Email or transcript missing'}, status=400)

            # Log the email data to track it
            logger.info(f"Sending transcript to: {email}")

            # Send the email
            send_mail(
                subject="Your Chat Transcript",
                message=transcript,
                from_email='krizzjain@gmail.com',  # Replace with your Gmail address
                recipient_list=[email],
                fail_silently=False,  # Use False for debugging; True in production
            )

            # Log success
            logger.info(f"Transcript sent to {email}")
            return JsonResponse({'success': True})

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    logger.error(f"Invalid request method: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)
