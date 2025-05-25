import streamlit as st
import os
import html
from streamlit_chat import message 
import json 
import traceback 

# For password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# --- Firebase Initialization (Simplified for this test, focusing on UI rendering) ---
app_id_global = 'default-app-id-local-dev' 
db = None 
print(f"INFO: Using app_id_global: {app_id_global}")
print("INFO: Initializing with MOCK Firestore for UI rendering test.")
_mock_db_users_store = {} 

class MockFirestoreDocument:
    def __init__(self, doc_id, data=None):
        self.id = doc_id; self._data = data if data is not None else {}; self._exists = data is not None
    def get(self): return self 
    def to_dict(self): return self._data
    @property 
    def exists(self): return self._exists
    def set(self, data_to_set):
        global _mock_db_users_store
        if self.id: _mock_db_users_store[self.id] = data_to_set
        self._data = data_to_set; self._exists = True
        print(f"MOCK_DB: Set data for {self.id}: {data_to_set}")

class MockFirestoreQuery:
    def __init__(self, field, op, value):
        self._results = []
        if field == "email" and op == "==" and value in _mock_db_users_store:
            self._results.append(MockFirestoreDocument(value, _mock_db_users_store[value]))
    def stream(self): return self._results
    def get(self): return self._results

class MockFirestoreCollection:
    def document(self, doc_id=None):
        if doc_id: return MockFirestoreDocument(doc_id, _mock_db_users_store.get(doc_id))
        raise ValueError("Mock document requires an ID for user collection.")
    def where(self, field, op, value): return MockFirestoreQuery(field, op, value)
    def add(self, data): 
        doc_id = os.urandom(10).hex(); _mock_db_users_store[doc_id] = data
        print(f"MOCK_DB: Added new doc with auto-ID {doc_id}")
        return MockFirestoreDocument(doc_id, data)

class MockDB: 
    def collection(self, collection_name): 
        print(f"MOCK_DB: Accessing collection '{collection_name}'")
        return MockFirestoreCollection()
db = MockDB() 

USER_CREDENTIALS_COLLECTION = f"artifacts/{app_id_global}/user_auth_credentials"

# --- Placeholder for gemini_handler and EDI_SPEC_DETAILS_MAP ---
# These are not critical for testing the login page rendering itself.
EDI_SPEC_DETAILS_MAP = {}
LOCAL_SPEC_OPTIONS_MAP = {"Select a Specification...": None}
def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None):
    return f"(Placeholder) Response to: '{html.escape(user_input)}'"

def load_css(file_path):
    # For this test, let's ensure CSS is NOT loaded to rule it out.
    print(f"DEBUG_MAIN_APP: CSS loading at '{file_path}' is SKIPPED for this minimal test.")
    # if os.path.exists(file_path):
    #     with open(file_path, "r", encoding='utf-8') as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # else: print(f"Warning: CSS file not found at {file_path}")

def register_user(email, password):
    if not db: st.error("Database service is not available."); return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email); user_doc_snapshot = user_doc_ref.get() 
        if user_doc_snapshot.exists: return False, "Email already registered."
        user_doc_ref.set({"email": email, "hashed_password": generate_password_hash(password)})
        return True, "Registration successful! Please login."
    except Exception as e: print(f"Error during registration: {e}"); traceback.print_exc(); return False, f"Registration failed: An unexpected error occurred."

def login_user(email, password):
    if not db: st.error("Database service is not available."); return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email); user_doc_snapshot = user_doc_ref.get() 
        if user_doc_snapshot.exists: 
            user_data = user_doc_snapshot.to_dict()
            if user_data and check_password_hash(user_data.get("hashed_password", ""), password): return True, "Login successful!"
            return False, "Incorrect password."
        return False, "Email not found."
    except Exception as e: print(f"Error during login: {e}"); traceback.print_exc(); return False, f"Login failed: An unexpected error occurred."

def display_login_page():
    print("DEBUG_MAIN_APP: >>> display_login_page() CALLED <<<") 
    st.subheader("Login")
    
    # Using st.form for the login inputs and button
    with st.form("login_form_minimal_test_v2", clear_on_submit=True): 
        email = st.text_input("Email", key="login_email_minimal_test_v2")
        password = st.text_input("Password", type="password", key="login_password_minimal_test_v2")
        submit_button = st.form_submit_button("Login")

        if submit_button: # This block is now inside the form
            print("DEBUG_MAIN_APP: Login form submitted.")
            if not email or not password: 
                st.error("Please enter both email and password.")
            else:
                success, message_text = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.page = "chat" 
                    st.success(message_text)
                    st.rerun() # Rerun to navigate and clear form
                else: 
                    st.error(message_text)
    
    print("DEBUG_MAIN_APP: About to render 'Register here' button (minimal test).") 
    # This button is OUTSIDE the form
    if st.button("Don't have an account? Register here.", key="goto_register_btn_minimal_test_v2"):
        print("DEBUG_MAIN_APP: 'Register here' button CLICKED (minimal test).") 
        st.session_state.page = "register"
        st.rerun()
    print("DEBUG_MAIN_APP: 'Register here' button rendering attempted (minimal test).") 
    print("DEBUG_MAIN_APP: >>> display_login_page() FINISHED <<<") 

# --- display_register_page and display_chat_app_page are stubs for this minimal test ---
def display_register_page():
    st.write("This is the register page (minimal test). Click below to go to Login.")
    if st.button("Go to Login", key="minimal_goto_login_from_register"):
        st.session_state.page = "login"
        st.rerun()

def display_chat_app_page():
    st.write(f"Welcome to chat, {st.session_state.get('user_email','User')} (minimal test).")
    if st.button("Logout", key="minimal_logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.page = "login"
        st.rerun()


def main():
    st.set_page_config(layout="centered", page_title="Volvo Cars EDI AI Assistant - Button Test")
    load_css(os.path.join("assets", "style.css")) # CSS loading is SKIPPED by the function itself

    print("DEBUG_MAIN_APP: In main() - Forcing LOGIN page display for button test.")
    
    # Initialize necessary session state variables if they don't exist
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    # --- FORCED PAGE DISPLAY BASED ON SESSION STATE (for minimal test) ---
    # This simplified routing is to ensure the button navigation works.
    if st.session_state.page == "register":
        display_register_page()
    else: # Default to login
        st.session_state.page = "login" # Ensure it's set
        display_login_page()


if __name__ == "__main__":
    main()
