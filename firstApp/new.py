import json

import random
import re
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup

from django.conf import settings
from django.http import FileResponse

from django.views.static import serve
import openai
import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from deep_translator import GoogleTranslator
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline, 
    Trainer, 
    TrainingArguments, 
    TextDataset, 
    DataCollatorForLanguageModeling
)

import torch

from sentence_transformers import SentenceTransformer, util
from spellchecker import SpellChecker
from sklearn.model_selection import train_test_split
import logging







def fuzzy_match_query(query, dataset, threshold=80):
    """ Match the query with the dataset using fuzzywuzzy to handle typos. """
    matched_key, score = process.extractOne(query, dataset.keys())
    
    if score >= threshold:
        return dataset[matched_key]
    return None










# Seting the path for the Google Cloud service account JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firstApp/charged-kiln-445717-k7-0f017d9755cf.json"
project_id = "charged-kiln-445717-k7" 

def query_dialogflow(text, session_id="current-user-session"):
    """Send a text query to Dialogflow and return the response."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text
    except Exception as e:
        print(f"Dialogflow Error: {e}")
        return None
    



from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    """Translate the given text to the target language (Hindi or Marathi)."""
    try:
        # Using deep-translator's GoogleTranslator
        translated = GoogleTranslator(source='en', target=target_language).translate(text)
        return translated
    except Exception as e:
        print(f"Error translating to {target_language}: {e}")
        return text  # Return original text if translation fails

    





from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline, 
    Trainer, 
    TrainingArguments, 
    TextDataset, 
    DataCollatorForLanguageModeling
)

import torch

from sentence_transformers import SentenceTransformer, util
from spellchecker import SpellChecker
from sklearn.model_selection import train_test_split
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPT2Responder:
    def __init__(self, data_file, fine_tune_model_path="./fine_tuned_gpt_neo"):
        """
        Initialize the GPT model, tokenizer, and semantic search components.
        """
        logger.info("Loading GPT-Neo model and tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
        self.model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
        self.generator = pipeline(
            'text-generation', 
            model=self.model, 
            tokenizer=self.tokenizer
        )
        logger.info("GPT-Neo model loaded successfully.")

        # Load and process HTML data
        logger.info("Extracting and embedding HTML data...")
        self.text_chunks = self.extract_text_from_html_file(data_file)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.embedding_model.encode(self.text_chunks)
        logger.info("Data embedding completed.")

        # Initializing  spell checker
        self.spell_checker = SpellChecker()

        # Fine-tune the model using the extracted text
        self.fine_tune_model_path = fine_tune_model_path
        if not os.path.exists(self.fine_tune_model_path):
            logger.info("Fine-tuning GPT-Neo on the extracted dataset...")
            try:
                self.fine_tune_model(self.text_chunks)
                logger.info("Fine-tuning completed.")
            except Exception as e:
                logger.error(f"Fine-tuning failed: {e}")
                logger.info("Using the base GPT-Neo model without fine-tuning.")
        else:
            logger.info("Loading fine-tuned model...")
            try:
                self.model = AutoModelForCausalLM.from_pretrained(self.fine_tune_model_path)
                self.tokenizer = AutoTokenizer.from_pretrained(self.fine_tune_model_path)
                self.generator = pipeline(
                    'text-generation', 
                    model=self.model, 
                    tokenizer=self.tokenizer
                )
                logger.info("Fine-tuned model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load fine-tuned model: {e}")
                logger.info("Using the base GPT-Neo model instead.")

    def fine_tune_model(self, text_chunks):
        """
        Fine-tune the GPT-Neo model on the provided text chunks.
        """
        # Save the text chunks to a temporary file for fine-tuning
        fine_tune_data_file = "fine_tune_dataset.txt"
        with open(fine_tune_data_file, "w", encoding="utf-8") as f:
            for chunk in text_chunks:
                f.write(chunk + "\n")

        # Add specific examples for concise answers
        with open(fine_tune_data_file, "a", encoding="utf-8") as f:
            f.write('''What are the social initiatives by Vidyalankar?\nSocial Initiatives:\n1. Polio Drive\n2. Distribution of Paper Bags\n3. Swaccha Bharat\n4. Tree Plantation\n5. Say No to Plastic\n6. Road Safety Awareness\n''')
            f.write("Who is the founder of VSIT team?\nPeople VSIT Team-Founders:\n1. C S Deshpande 1998-2005\n2. S C Deshpande 2005-2016\n")
            f.write("Who is the secretary of VSIT team?\nAvinash Chatorikar - Secretary\n")
            f.write("Who is the chairperson of Vidyalankar Dnyanapeeth Trust?\nRashmi Deshpande - Chairperson\n")
            f.write("Who are the trustees of Vidyalankar Dnyanapeeth Trust?\nNamrata Deshpande - Trustee\nVishwas Deshpande - Trustee\nKeshav Kulkarni - Trustee\n")
            f.write("Who is the director of Vidyalankar Educational Campus?\nMilind Tadvalkar - Director\n")
            f.write("Who is the principal of VSIT?\nDr(Mrs). Rohini Kelkar - Principal\n")
            f.write("Who is the vice principal of Information Technology at VSIT?\nProf. Asif Rampurawala - Vice Principal-Information Technology\n")
            f.write("Who is the vice principal of Commerce & Management at VSIT?\nProf. Vijay Gawde - Vice Principal-Commerce & Management\n")

        # Split the dataset into training and validation sets
        with open(fine_tune_data_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        train_texts, val_texts = train_test_split(lines, test_size=0.1)

        # Save the datasets to temporary files
        with open("train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_texts)
        with open("val.txt", "w", encoding="utf-8") as f:
            f.writelines(val_texts)

        # Loading the datasets
        train_dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path="train.txt",
            block_size=128
        )
        val_dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path="val.txt",
            block_size=128
        )

        # Defining data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        # Define training arguments
        training_args = TrainingArguments(
            output_dir=self.fine_tune_model_path,
            overwrite_output_dir=True,
            num_train_epochs=5,  # Increased epochs for better fine-tuning
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            save_steps=10_000,
            save_total_limit=2,
            evaluation_strategy="epoch",
            logging_dir="./logs",
            logging_steps=500,
            fp16=torch.cuda.is_available(),  # Enable mixed precision training if GPU is available
        )

        # Initialize the Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
        )

        # Fine-tune the model
        trainer.train()

        # Save the fine-tuned model
        trainer.save_model(self.fine_tune_model_path)
        self.tokenizer.save_pretrained(self.fine_tune_model_path)

        # Clean up temporary files
        os.remove(fine_tune_data_file)
        os.remove("train.txt")
        os.remove("val.txt")

    def correct_spelling(self, query):
        """
        Correct spelling errors in the query.
        """
        corrected_words = []
        for word in query.split():
            corrected_word = self.spell_checker.correction(word)
            if corrected_word is not None:  # Ensure the corrected word is not None
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)  # Use the original word if correction is None
        corrected_query = " ".join(corrected_words)
        return corrected_query

    def extract_text_from_html_file(self, file_path):
        """
        Extract and clean text from an HTML file, preserving structure.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_html = file.read()

        soup = BeautifulSoup(raw_html, "html.parser")

        # Remove scripts and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Extract and clean visible text
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Group related lines (e.g., headings and their descriptions)
        grouped_lines = []
        current_group = []
        for line in lines:
            if line.endswith(":") or line.endswith(".") or line.isupper():  # Likely a heading
                if current_group:
                    grouped_lines.append(" ".join(current_group))
                    current_group = []
                current_group.append(line)
            else:
                current_group.append(line)
        if current_group:
            grouped_lines.append(" ".join(current_group))

        return grouped_lines

    def filter_relevant_sections(self, query, text_chunks):
        """
        Filter text chunks that contain keywords related to the query.
        """
        # Extract keywords from the query
        keywords = query.lower().split()
        relevant_chunks = []
        for chunk in text_chunks:
            if any(keyword in chunk.lower() for keyword in keywords):
                relevant_chunks.append(chunk)
        return relevant_chunks

    def query(self, prompt):
        """
        Generate a response to the given prompt using semantic search and GPT-Neo.
        """
        logger.info(f"Received prompt: {prompt}")
        try:
            # Correct spelling in the query
            prompt = self.correct_spelling(prompt)

            # Filter relevant sections based on keywords
            relevant_sections = self.filter_relevant_sections(prompt, self.text_chunks)
            logger.info(f"Relevant sections: {relevant_sections}")

            # If relevant sections are found, perform semantic search on them
            if relevant_sections:
                relevant_embeddings = self.embedding_model.encode(relevant_sections)
                query_embedding = self.embedding_model.encode(prompt)
                scores = util.cos_sim(query_embedding, relevant_embeddings)
                best_match_idx = scores.argmax().item()
                response = relevant_sections[best_match_idx]
                return response

            # Fallback to GPT-Neo only if no relevant text is found
            refined_prompt = (
                f"Context: {relevant_sections}\n"
                f"User Query: {prompt}\n" 
                f"Answer the user query in the following format and do not include any extra information:\n"
                f"People VSIT Team-Founders:\n1. C S Deshpande 1998-2005\n2. S C Deshpande 2005-2016\n"
            )
            logger.info(f"Refined prompt: {refined_prompt}")

            # Generate text using GPT-Neo
            generated = self.generator(
                refined_prompt,
                max_new_tokens=50,  # Increased token limit for more detailed responses
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.5,
                top_p=0.5,
                top_k=30
            )

            # Extract and clean the generated response
            response = generated[0]['generated_text'].replace(refined_prompt, "").strip()
            response = self.clean_response(response)

            # Validate response
            if not response or len(response.split()) < 5:
                return "I'm sorry, I couldn't generate a proper response. Please check our website for more information."

            return response
        except Exception as e:
            logger.error(f"Error: {e}")
            return "There was an issue generating a response. Please try again later."

    def clean_response(self, response):
        """
        Clean up the response by removing any repetitive or malformed content.
        """
        # Remove repeated query mentions or invalid sequences
        response = response.split("Query:")[0]
        response = response.split("Answer:")[-1].strip()
        # Trim to only the required information
        if "People VSIT Team-Founders:" in response:
            response = response.split("People VSIT Team-Founders:")[1].strip()
            response = "People VSIT Team-Founders:\n" + response.split("\n")[0] + "\n" + response.split("\n")[1]
        return response.strip()


# Example usage
data_file_path = "firstApp/vsit_data/about.html.txt"
gpt2_responder = GPT2Responder(data_file_path)
response = gpt2_responder.query("Who is the founder of VSIT team?")
print("Final Response:", response)


from django.conf import settings
from django.http import FileResponse

# Load the course PDFs from the JSON file
def load_course_pdfs():
    json_path = os.path.join(settings.BASE_DIR, 'firstApp/static/course_pdf.json')
    with open(json_path, 'r') as f:
        return json.load(f)


def load_course_aliases():
    json_path = os.path.join(settings.BASE_DIR, 'firstApp/static/course_alias.json')
    with open(json_path, 'r') as f:
        return json.load(f)

course_aliases = load_course_aliases()
course_pdfs = load_course_pdfs()

course_aliasess = {
    "bscit": ["bscit", "b.scit", "b.sc.it", "b.sc. it", "b sc it", "bsc it","bsc it"],
    "bscds": ["bscds", "b.scds", "b.sc.ds", "b sc ds", "bsc data science","bsc ds"],
    "bms": ["bms", "b.m.s"],
    "bcom": ["bcom", "b.com", "b com", "bcom accounting finance", "bcom banking insurance"],
    "bfm": ["bfm", "b.f.m"],
    "ba": ["ba", "b.a", "b.a.", "b.a mass communication", "ba multimedia","Ba","BA"],
    "mscit": ["msc it", "m.sc.it", "m.sc. it", "msc information technology","Msc It","MSC IT","Msc It"],
    "mcom": ["mcom", "m.com", "m com","MCOM","M COM","M com"],
    "ma": ["ma", "m.a", "m.a.","MA","Ma"]
}

# Session state (in production, use a persistent session or user context)
session_state = {
    "course": None,
    "percentage": None,
    "stream": None,
    "eligibility_mode": False
}
def extract_parameters(user_query):
    user_query = user_query.lower()

    # Extract course only if not already set
    if not session_state["course"]:
        for course, aliases in course_aliasess.items():
            if any(alias in user_query for alias in aliases):
                session_state["course"] = course
                break

    # Extract percentage only if not already set
    if session_state["percentage"] is None:
        match = re.search(r'(\d{1,3}(?:\.\d+)?)\s*%', user_query)
        if match:
            session_state["percentage"] = float(match.group(1))
        else:
            match = re.search(r'\b(\d{2,3})\b', user_query)
            if match:
                percent = int(match.group(1))
                if 0 <= percent <= 100:
                    session_state["percentage"] = percent

    # Extract stream only if not already set
    if not session_state["stream"]:
        for stream in ["science", "commerce", "arts"]:
            if stream in user_query:
                session_state["stream"] = stream.capitalize()


def check_eligibility():
    course = session_state["course"]
    percentage = session_state["percentage"]
    stream = session_state["stream"]

    if course == "bscit":
        if stream == "Science" and percentage >= 45:
            return "You are eligible for B.Sc. IT. 🎉"
        return "You need to have Science stream and at least 45% to be eligible for B.Sc. IT."

    elif course == "bscds":
        if stream == "Science" and percentage >= 45:
            return "You are eligible for B.Sc. Data Science. 🎉"
        return "You need to have Science stream and at least 45% to be eligible for B.Sc. Data Science."

    elif course == "bms":
        if percentage >= 45:
            return "You are eligible for B.M.S. 🎉"
        return "You need at least 45% to be eligible for B.M.S."

    elif course in ["bcom", "bfm"]:
        if percentage >= 45:
            return f"You are eligible for {'B.Com.' if course == 'bcom' else 'B.F.M.'} 🎉"
        return f"You need at least 45% to be eligible for {'B.Com.' if course == 'bcom' else 'B.F.M.'}"

    elif course == "ba":
        if stream in ["Science", "Commerce", "Arts"]:
            return "You are eligible for B.A. (Mass Communication/Multimedia). 🎉"
        return "Please specify a valid stream."

    elif course in ["mscit", "mcom", "ma"]:
        return f"Eligibility depends on your undergraduate background. Please check university criteria for {course.upper()}."

    return "You are not eligible for the selected course."





def get_response(user_query, language='en'):
    """Get response based on user query."""
    user_query = user_query.lower()

    # Handle specific queries locally
    if 'weather' in user_query:
        # Extract city name using regex
        match = re.search(r'weather\s*(?:in)?\s*(\w+)', user_query)
        if match:
            city = match.group(1)  # Extracts the city name
            return fetch_weather(city)
        else:
            return "Please specify a city for the weather report."

    # Handle PDF/Brochure requests
    if 'pdf' in user_query or 'brochure' in user_query or 'documents' in user_query:
        for coursea, aliases in course_aliases.items():
            for alias in aliases:
                print(f"Checking if '{alias}' is in '{user_query}'")  # Debugging line
                if alias in user_query:
                    pdf_link = course_pdfs.get(coursea)
                    if pdf_link:
                        absolute_pdf_link = f"{settings.MEDIA_URL}{os.path.basename(pdf_link)}"
                        return f"Here is the PDF for {coursea}: <a href='{absolute_pdf_link}' download>Download PDF</a>"
                    else:
                        return f"Sorry, the PDF/Brochure for {coursea} is not available."
                    
     # Trigger eligibility mode if keywords found
    # Handle Eligibility mode
    eligibility_keywords = ["eligible", "eligibility", "admission", "apply", "can i take", "requirement", "can i get", "qualification"]
    if session_state.get("eligibility_mode") or any(word in user_query for word in eligibility_keywords):
        session_state["eligibility_mode"] = True

        # Check for new course and reset stream/percentage if course changed
        for course, aliases in course_aliasess.items():
            if any(alias in user_query for alias in aliases):
                if session_state["course"] != course:
                    session_state["course"] = course
                    session_state["percentage"] = None
                    session_state["stream"] = None
                break

        # Extract any new parameters
        extract_parameters(user_query)

        # If all info is available, respond with eligibility result
        if session_state["course"] and session_state["percentage"] is not None and session_state["stream"]:
            session_state["eligibility_mode"] = False
            return check_eligibility()

        # Prompt for missing inputs
        if not session_state["course"]:
            return "Which course are you interested in? (e.g., B.Sc. IT, M.Sc. IT, M.Com, MA)?"
        elif session_state["percentage"] is None:
            return "Please let me know your 12th percentage."
        elif not session_state["stream"]:
            return "Please let me know your stream (Science, Commerce, or Arts)."

            
    # Use Dialogflow for other queries
    dialogflow_response = query_dialogflow(user_query)
    print(f"Dialogflow response: {dialogflow_response}")

    # Check if Dialogflow response is the specific phrase
    if dialogflow_response.strip() == "Sorry, I didn't get that. Can you rephrase?":
        print("Fallback triggered. Using GPT-Neo for response...")
        # Load GPT-Neo model only when needed
        data_file_path = "firstApp/vsit_data/about.html.txt"  # Adjust this as per your project structure
        gpt2_responder = GPT2Responder(data_file_path)
        gpt_response = gpt2_responder.query(user_query)
        return gpt_response

    if dialogflow_response:
        print(f"Returning Dialogflow response: {dialogflow_response}")
        if language == 'hi':
            dialogflow_response = translate_text(dialogflow_response, 'hi')
        elif language == 'mr':
            dialogflow_response = translate_text(dialogflow_response, 'mr')
        return dialogflow_response

    return "Sorry, I couldn't process your query. Please try again later."

from django.http import FileResponse

# Add this function to download the PDF file
def download_pdf(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf') 



















def send_name_to_dialogflow(user_name):
    try:
        session_id = "current-user-session"
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
       
        
        # Specify the project ID (replace with your actual Dialogflow project ID)
        
        session = session_client.session_path(project_id, session_id)
        
        # Prepare the text input to send to Dialogflow
        text_input = dialogflow.TextInput(text=f" my name is {user_name}.", language_code='en')
        query_input = dialogflow.QueryInput(text=text_input)
        
        # Send the query to Dialogflow
        response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
        
        # Handle the response (you can process it or print it here)
        print(f"Dialogflow Response: {response.query_result.fulfillment_text}")
        
        # Return the response text from Dialogflow
        return response.query_result.fulfillment_text
    


    except Exception as e:
        print(f"Error sending to Dialogflow: {e}")
        return "There was an error communicating with Dialogflow."
    

def fetch_weather(city):
    """ Fetch the current weather for a given city using Open-Meteo API. """
    # Map cities to their coordinates
    city_coordinates = {
        'mumbai': (19.0760, 72.8777),
        'thane': (19.2183, 72.9785),
        'navi mumbai': (19.0360, 73.0330)
    }
    
    # Normalize city input
    city = city.lower().strip()

    # Check if the city is in the predefined list
    if city in city_coordinates:
        latitude, longitude = city_coordinates[city]
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=Asia%2FKolkata"
        
        try:
            # Fetch the weather data from the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            
            data = response.json()
            temperature = data['current_weather']['temperature']
            weather_code = data['current_weather']['weathercode']
            
            weather_descriptions = {
                0: "clear sky",
                1: "mainly clear",
                2: "partly cloudy",
                3: "overcast",
                45: "fog",
                48: "depositing rime fog",
                51: "light drizzle",
                53: "moderate drizzle",
                55: "dense drizzle",
                56: "freezing drizzle",
                57: "freezing fog",
                61: "light rain",
                63: "moderate rain",
                65: "heavy rain",
                66: "freezing rain",
                67: "heavy freezing rain",
                71: "light snow",
                73: "moderate snow",
                75: "heavy snow",
                77: "snow grains",
                80: "light rain showers",
                81: "moderate rain showers",
                82: "heavy rain showers",
                85: "light snow showers",
                86: "heavy snow showers",
                95: "thunderstorms",
                96: "thunderstorms with hail",
                99: "thunderstorms with heavy hail"
            }
            
            weather_description = weather_descriptions.get(weather_code, "unknown weather condition")
            return f"The current temperature in {city.title()} is {temperature}°C with {weather_description}."
        
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

    return f"Sorry, I don't have weather data for {city.title()}."
