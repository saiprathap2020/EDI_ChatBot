# gemini_handler.py
import google.generativeai as genai
import os
# from dotenv import load_dotenv # Not needed for Streamlit Cloud deployment if secrets are used
import traceback
import requests 
import re 
import html
import streamlit as st # Import Streamlit to access st.secrets
import json # MODIFICATION: Added import for json module

# --- Load Environment Variables & Configure Gemini ---
# For Streamlit Cloud deployment, secrets are set via st.secrets or as environment variables
# load_dotenv() # Keep for local testing if you use a .env file

GOOGLE_API_KEY = None
# 1. Try to get from Streamlit secrets (preferred for Streamlit Cloud)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    print("INFO: Loaded GOOGLE_API_KEY from Streamlit secrets.")
# 2. Fallback to environment variable (useful for other deployment platforms or local if .env is not used)
elif os.getenv("GOOGLE_API_KEY"):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print("INFO: Loaded GOOGLE_API_KEY from environment variable.")

if not GOOGLE_API_KEY:
    print("WARN: GOOGLE_API_KEY not found in Streamlit secrets or environment variables. AI features may fail.")
    model = None
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("SUCCESS: Gemini API configured.")
    except Exception as e:
        print(f"ERROR: Failed to configure Gemini API with key: {e}")
        model = None


# --- FastAPI Endpoint ---
# This should be your live Render URL (or other deployed FastAPI backend URL)
# For Streamlit Cloud, set this as a secret: FASTAPI_BASE_URL
fastapi_url_from_secrets = st.secrets.get("FASTAPI_BASE_URL") if "FASTAPI_BASE_URL" in st.secrets else None
FASTAPI_BASE_URL = fastapi_url_from_secrets or os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000") # Default for local

if FASTAPI_BASE_URL == "http://127.0.0.1:8000" and not fastapi_url_from_secrets and not os.getenv("FASTAPI_BASE_URL"):
    print("WARN: FASTAPI_BASE_URL is using default localhost. For deployed version, set this secret in Streamlit Cloud or as an env var.")
elif fastapi_url_from_secrets:
    print(f"INFO: Loaded FASTAPI_BASE_URL from Streamlit secrets: {FASTAPI_BASE_URL}")
elif os.getenv("FASTAPI_BASE_URL"):
     print(f"INFO: Loaded FASTAPI_BASE_URL from environment variable: {FASTAPI_BASE_URL}")


def extract_segment_from_query(user_input):
    cleaned_input = user_input.upper()
    phrases_to_remove = ["EXPLAIN ME ABOUT", "WHAT IS", "TELL ME ABOUT", "EXPLAIN"]
    for phrase in phrases_to_remove:
        if cleaned_input.startswith(phrase):
            cleaned_input = cleaned_input[len(phrase):].strip()
    if cleaned_input.endswith(" SEGMENT"):
        cleaned_input = cleaned_input[:-len(" SEGMENT")].strip()
    
    match_plus = re.search(r"([A-Z0-9]{2,6}\+[A-Z0-9]{1,3})", cleaned_input)
    if match_plus: return match_plus.group(1)
    words = cleaned_input.split()
    for word in words:
        if word.isupper() and 2 <= len(word) <= 6 and word not in ["IS", "A", "THE", "AN", "FOR", "EDI", "ME", "ABOUT"]:
            return word
    return None

def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None):
    print(f"\nGEMINI_HANDLER: Input='{user_input}', SpecOpt='{spec_option}', UseAI={use_gemini_model}, SpecDetails={spec_details}")

    normalized_input = user_input.lower()
    url_keywords = ["specification url", "specs url", "guidelines url", "documentation url", "link for edi specs"]
    for keyword in url_keywords:
        if keyword in normalized_input:
            return "You can find the Volvo Cars EDI specifications at: https://explore.hcltech.com/EDI/cars/specifications.html"

    try:
        if not use_gemini_model: # LOCAL DATA ONLY MODE (via FastAPI)
            print("    MODE: Local Data via FastAPI")
            
            if not spec_details:
                print("    Local Mode: No specific spec_details provided from UI. Asking user to select from dropdown.")
                return "In Local Data mode, please select a specific EDI specification from the dropdown to query its details."

            if user_input.startswith(f"Show information for {spec_details.get('display','the selected specification')}"):
                return f"You've selected {spec_details.get('display','the specification')}. Please ask about a specific segment (e.g., 'What is UNH?')."

            segment_to_explain = extract_segment_from_query(user_input)
            if not segment_to_explain:
                return f"Could not identify a specific segment in your query '{user_input}' for {spec_details.get('display','the selected specification')}. Please ask about a specific segment (e.g., 'BGM', 'NAD+SE')."

            print(f"    Local Mode: Extracted segment '{segment_to_explain}' for spec '{spec_details.get('display', 'Unknown Spec')}'")
            
            payload = {
                "segment": segment_to_explain, 
                "standard": spec_details["standard"],
                "message_type": spec_details["message_type"], 
                "version": spec_details.get("version", "")
            }
            print(f"    FastAPI Request: POST to {FASTAPI_BASE_URL}/explain_segment/ with payload: {payload}")
            
            api_response = None # Initialize api_response
            try:
                api_response = requests.post(f"{FASTAPI_BASE_URL}/explain_segment/", json=payload, timeout=15)
                print(f"    FastAPI Status Code: {api_response.status_code}")
                api_response.raise_for_status() 
                data = api_response.json() # This line can raise json.JSONDecodeError
                print(f"    FastAPI Response Data: {data}")
                return data.get("explanation", f"No explanation found via API for segment '{segment_to_explain}' in {spec_details.get('display', 'the selected specification')}.")
            except requests.exceptions.ConnectionError:
                print(f"    ERROR: FastAPI Connection Error to {FASTAPI_BASE_URL}.")
                return "Error: Could not connect to the local data service. Please ensure it's running and the URL is correct."
            except requests.exceptions.HTTPError as http_err:
                print(f"    ERROR: FastAPI HTTP Error: {http_err}. Response: {api_response.text if api_response else 'N/A'}")
                return f"Error communicating with local data service (HTTP {api_response.status_code if api_response else 'N/A'}). Please check service logs."
            except requests.exceptions.RequestException as e:
                print(f"    ERROR: FastAPI Request Error: {e}")
                return f"Error communicating with local data service: {e}"
            except json.JSONDecodeError as e: # Catch error if response is not valid JSON
                print(f"    ERROR: Could not decode JSON response from FastAPI: {e}. Response text: {api_response.text if api_response is not None else 'N/A'}")
                return "Error: Received an invalid response from the local data service."


        # --- AI Model Mode ---
        # ... (rest of AI mode logic remains the same) ...
        print("    MODE: AI Model (Gemini)")
        if not model: 
            return "AI model is currently unavailable. API key might be missing or invalid."

        prompt_context = ""
        if spec_details: 
            prompt_context = f"The user might be asking in the context of {spec_details.get('display','')} ({spec_details.get('standard','')}-{spec_details.get('message_type','')} {spec_details.get('version','')})."

        prompt = f"""You are an expert AI assistant for Volvo Cars EDI (Electronic Data Interchange).
Your primary goal is to provide accurate and helpful information regarding EDI standards and practices relevant to Volvo Cars suppliers.
{prompt_context}
Be concise, clear, and directly answer the user's question.

User's question: "{html.escape(user_input)}"

Answer:"""
        
        print("\n    --- Sending Prompt to Gemini ---")
        print("    Prompt length:", len(prompt))
        print("    --------------------------------\n")

        gen_response = model.generate_content(prompt)
        print("    --- Received Response from Gemini ---")
        response_text = ""
        if gen_response.candidates:
            candidate = gen_response.candidates[0]
            if candidate.finish_reason == 'SAFETY': 
                response_text = "Response blocked for safety."
                if hasattr(candidate, 'safety_ratings'): print(f"    Safety ratings: {candidate.safety_ratings}")
            elif candidate.content and candidate.content.parts: 
                response_text = candidate.content.parts[0].text.strip()
            else: 
                response_text = "AI returned empty/unexpected content."
        else: 
            response_text = "AI returned no candidates."
            if hasattr(gen_response, 'prompt_feedback') and gen_response.prompt_feedback and gen_response.prompt_feedback.block_reason:
                 response_text += f" Reason: {gen_response.prompt_feedback.block_reason}"
        
        print(f"    Returning AI Response: {response_text[:100]}...")
        return response_text if response_text else " "

    except Exception as e:
        print(f"!!! ERROR in get_gemini_response: {type(e).__name__}: {e} !!!"); traceback.print_exc()
        return "Critical error in handler. Check logs."
