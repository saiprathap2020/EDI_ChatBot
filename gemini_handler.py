# gemini_handler.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import requests # For calling FastAPI
import re # For extracting segment code
import html # For escaping

# --- Load Environment Variables & Configure Gemini ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- FastAPI Endpoint ---
FASTAPI_BASE_URL = "https://volvo-edi-fastapi-backend.onrender.com" # Your FastAPI app's address

def extract_segment_from_query(user_input):
    """
    Simple heuristic to extract a potential segment code from user input.
    Looks for uppercase words, or words like NAD+SE.
    """
    cleaned_input = user_input.upper()
    phrases_to_remove = ["EXPLAIN ME ABOUT", "WHAT IS", "TELL ME ABOUT", "EXPLAIN"]
    for phrase in phrases_to_remove:
        if cleaned_input.startswith(phrase):
            cleaned_input = cleaned_input[len(phrase):].strip()
    if cleaned_input.endswith(" SEGMENT"):
        cleaned_input = cleaned_input[:-len(" SEGMENT")].strip()
    
    match_plus = re.search(r"([A-Z0-9]{2,6}\+[A-Z0-9]{1,3})", cleaned_input)
    if match_plus:
        return match_plus.group(1)

    words = cleaned_input.split()
    for word in words:
        if word.isupper() and len(word) >= 2 and len(word) <= 6:
            if word not in ["IS", "A", "THE", "AN", "FOR", "EDI", "ME", "ABOUT"]: # Avoid common words
                return word
    return None

# --- Main Response Function ---
# MODIFICATION: Added spec_details=None to the function signature
def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None):
    print("\n" + "="*50)
    print(f"--- GEMINI_HANDLER: Received ---")
    print(f"    User Input: '{user_input}'")
    print(f"    Spec Option Key (from UI): '{spec_option}'") # This is the internal key like "DELFOR_D04A"
    print(f"    Spec Details (from UI): {spec_details}") # This is the dict with standard, type, version
    print(f"    Use AI Model: {use_gemini_model}")
    print("="*50)

    normalized_input = user_input.lower()
    url_keywords = ["specification url", "specs url", "guidelines url", "documentation url"]
    for keyword in url_keywords:
        if keyword in normalized_input:
            return "You can find the Volvo Cars EDI specifications at: https://explore.hcltech.com/EDI/cars/specifications.html"

    try:
        if not use_gemini_model: # LOCAL DATA ONLY MODE (via FastAPI)
            print("    MODE: Local Data via FastAPI")
            
            if not spec_details:
                print("    Local Mode: No specific spec_details provided. Asking user to select from dropdown.")
                return "In Local Data mode, please select a specific EDI specification from the dropdown to query its details."

            # Handle auto-query from dropdown selection
            if user_input.startswith(f"Show information for {spec_details.get('display', 'the selected specification')}"):
                return f"You've selected {spec_details.get('display', 'the specification')}. Please ask about a specific segment (e.g., 'What is UNH?')."

            segment_to_explain = extract_segment_from_query(user_input)
            if not segment_to_explain:
                return f"Could not identify a specific segment in your query '{user_input}' for {spec_details.get('display', 'the selected specification')}. Please ask about a specific segment (e.g., 'BGM', 'NAD+SE')."

            print(f"    Local Mode: Extracted segment '{segment_to_explain}' for spec '{spec_details.get('display', 'Unknown Spec')}'")
            
            payload = {
                "segment": segment_to_explain,
                "standard": spec_details["standard"],
                "message_type": spec_details["message_type"],
                "version": spec_details.get("version", "") # Ensure version is present, default to empty string
            }
            print(f"    FastAPI Request Payload: {payload}")
            
            try:
                response = requests.post(f"{FASTAPI_BASE_URL}/explain_segment/", json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                print(f"    FastAPI Response Data: {data}")
                return data.get("explanation", f"No explanation found via API for segment '{segment_to_explain}' in {spec_details.get('display', 'the selected specification')}.")
            except requests.exceptions.ConnectionError:
                print("    ERROR: FastAPI Connection Error. Is the FastAPI server running at " + FASTAPI_BASE_URL + "?")
                return "Sorry, I could not connect to the local data service. Please ensure it's running."
            except requests.exceptions.RequestException as e:
                print(f"    ERROR: FastAPI Request Error: {e}")
                return f"Sorry, there was an error communicating with the local data service: {e}"
            except Exception as e:
                print(f"    ERROR: Error processing FastAPI response or other issue: {e}")
                traceback.print_exc()
                return "Sorry, an unexpected error occurred while fetching local data."

        # --- AI Model Mode ---
        print("    MODE: AI Model (Gemini)")
        prompt_context = ""
        if spec_details: # Use spec_details for context if available
            prompt_context = f"The user might be asking in the context of {spec_details.get('display','')} ({spec_details.get('standard','')}-{spec_details.get('message_type','')} {spec_details.get('version','')})."

        prompt = f"""You are an expert AI assistant for Volvo Cars EDI (Electronic Data Interchange).
Your primary goal is to provide accurate and helpful information regarding EDI standards and practices relevant to Volvo Cars suppliers.
{prompt_context}
Be concise, clear, and directly answer the user's question.

User's question: "{html.escape(user_input)}"

Answer:"""
        
        print("\n    --- Sending Prompt to Gemini ---")
        print("    Prompt length:", len(prompt))
        # print(f"    Full Prompt:\n{prompt}") # Uncomment for debugging full prompt
        print("    --------------------------------\n")

        response = model.generate_content(prompt)
        print("    --- Received Response from Gemini ---")
        response_text = ""
        if response.candidates:
            candidate = response.candidates[0]
            if candidate.finish_reason == 'SAFETY':
                response_text = "I cannot provide a response to that request due to safety restrictions."
            elif candidate.content and candidate.content.parts:
                response_text = candidate.content.parts[0].text.strip()
            else:
                response_text = "The AI model returned content, but it was empty/unexpected."
        else:
            response_text = "The AI model did not return any candidates."
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
                 response_text += f" Reason: {response.prompt_feedback.block_reason}"
        
        print(f"    Returning AI Response: {response_text[:100]}...")
        return response_text if response_text else " "

    except Exception as e:
        print(f"\n!!! ERROR in get_gemini_response: {type(e).__name__}: {e} !!!")
        traceback.print_exc()
        return "Sorry, a critical error occurred. Please check terminal logs."