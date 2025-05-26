import streamlit as st
import os
import html
from streamlit_chat import message 
import json 
import traceback 

# For password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# --- Firebase Initialization (Simplified to MOCK for this UI test) ---
app_id_global = 'default-app-id-local-dev' 
db = None 
print(f"INFO: Using app_id_global: {app_id_global}")

_mock_db_users_store = {} 
print(f"INFO: Initializing MOCK Firestore. Current store: {_mock_db_users_store}")

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
        print(f"MOCK_DB_SET: User '{self.id}', Data: {data_to_set}. Current store: {_mock_db_users_store}")

class MockFirestoreQuery: # Not strictly needed for this test, but part of the mock
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

class MockDB: 
    def collection(self, collection_name): 
        print(f"MOCK_DB_ACCESS: Collection '{collection_name}'")
        return MockFirestoreCollection()
db = MockDB() 

USER_CREDENTIALS_COLLECTION = f"artifacts/{app_id_global}/user_auth_credentials"

# --- Placeholders for other parts of your app ---
EDI_SPEC_DETAILS_MAP = {} 
LOCAL_SPEC_OPTIONS_MAP = {"Select a Specification...": None}
def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None):
    return f"(Placeholder) Response to: '{html.escape(user_input)}'"

def load_css(file_path):
    print(f"DEBUG_MAIN_APP: CSS loading SKIPPED for this test.")
    # if os.path.exists(file_path):
    #     with open(file_path, "r", encoding='utf-8') as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # else: print(f"Warning: CSS file not found at {file_path}")

# --- Authentication Functions with Enhanced Debugging ---
def register_user(email, password):
    print(f"DEBUG_REGISTER: Attempting to register email: {email}")
    if not db: 
        st.error("Database service is not available (register_user)."); 
        print("DEBUG_REGISTER: DB object is None!")
        return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        user_doc_snapshot = user_doc_ref.get() 
        print(f"DEBUG_REGISTER: Checked for existing user '{email}'. Exists: {user_doc_snapshot.exists}")
        if user_doc_snapshot.exists: 
            return False, "Email already registered."
        
        hashed_password = generate_password_hash(password)
        user_doc_ref.set({"email": email, "hashed_password": hashed_password}) # MockDB set will print
        print(f"DEBUG_REGISTER: Registration successful for {email}.")
        return True, "Registration successful! Please login."
    except Exception as e: 
        print(f"ERROR_REGISTER: {e}"); traceback.print_exc()
        return False, f"Registration failed: An unexpected error occurred."

def login_user(email, password):
    print(f"DEBUG_LOGIN: Attempting to login email: {email}")
    if not db: 
        st.error("Database service is not available (login_user)."); 
        print("DEBUG_LOGIN: DB object is None!")
        return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        user_doc_snapshot = user_doc_ref.get() 
        print(f"DEBUG_LOGIN: Checked for user '{email}'. Exists: {user_doc_snapshot.exists}")
        if user_doc_snapshot.exists: 
            user_data = user_doc_snapshot.to_dict()
            print(f"DEBUG_LOGIN: User data found: {user_data is not None}")
            if user_data and check_password_hash(user_data.get("hashed_password", ""), password):
                print(f"DEBUG_LOGIN: Password MATCH for {email}")
                return True, "Login successful!"
            print(f"DEBUG_LOGIN: Password MISMATCH for {email}")
            return False, "Incorrect password."
        return False, "Email not found."
    except Exception as e: 
        print(f"ERROR_LOGIN: {e}"); traceback.print_exc()
        return False, f"Login failed: An unexpected error occurred."

# --- UI Functions (Simplified Keys for Debugging) ---
def display_login_page():
    print("DEBUG_MAIN_APP: >>> display_login_page() CALLED <<<") 
    st.subheader("Login")
    with st.form("login_form_debug_v4"): 
        email = st.text_input("Email", key="login_email_debug_v4")
        password = st.text_input("Password", type="password", key="login_password_debug_v4")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if not email or not password: st.error("Please enter both email and password.")
            else:
                success, message_text = login_user(email, password)
                if success:
                    st.session_state.logged_in = True; st.session_state.user_email = email; st.session_state.page = "chat" 
                    st.success(message_text); st.rerun() 
                else: st.error(message_text)
    
    print("DEBUG_MAIN_APP: About to render 'Register here' button.") 
    if st.button("Don't have an account? Register here.", key="goto_register_btn_debug_v4"):
        print("DEBUG_MAIN_APP: 'Register here' button CLICKED.") 
        st.session_state.page = "register"; st.rerun()
    print("DEBUG_MAIN_APP: 'Register here' button rendering attempted.") 
    print("DEBUG_MAIN_APP: >>> display_login_page() FINISHED <<<") 

def display_register_page():
    print("DEBUG_MAIN_APP: >>> display_register_page() CALLED <<<") 
    st.subheader("Register New Account")
    with st.form("register_form_debug_v4"): 
        email = st.text_input("Email", key="register_email_debug_v4")
        password = st.text_input("Password", type="password", key="register_password_debug_v4")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_debug_v4")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            if not email or not password or not confirm_password: st.error("Please fill in all fields.")
            elif password != confirm_password: st.error("Passwords do not match.")
            else:
                success, message_text = register_user(email, password)
                if success: st.success(message_text); st.session_state.page = "login"; st.rerun()
                else: st.error(message_text)
    if st.button("Already have an account? Login here.", key="goto_login_btn_debug_v4"):
        st.session_state.page = "login"; st.rerun()
    print("DEBUG_MAIN_APP: >>> display_register_page() FINISHED <<<") 

def display_chat_app_page(): # Stub for this test
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() CALLED <<<") 
    st.title("Chat App Page (Debug)")
    st.write(f"Welcome, {st.session_state.get('user_email', 'User')}!")
    if st.button("Logout", key="logout_debug_v4"):
        st.session_state.logged_in = False; st.session_state.user_email = None; st.session_state.page = "login"
        st.rerun()
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() FINISHED <<<") 

# --- Main App Router (Simplified for Debugging) ---
def main():
    st.set_page_config(layout="centered", page_title="Volvo Cars EDI AI Assistant - Auth Debug")
    load_css(os.path.join("assets", "style.css")) # CSS loading is skipped by the function

    # Initialize session state variables if they don't exist
    if "page" not in st.session_state:
        st.session_state.page = "login" 
        print(f"DEBUG_MAIN_APP: Initialized st.session_state.page to '{st.session_state.page}'")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        print(f"DEBUG_MAIN_APP: Initialized st.session_state.logged_in to {st.session_state.logged_in}")
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    
    print(f"DEBUG_MAIN_APP: In main() - Current page: '{st.session_state.page}', Logged in: {st.session_state.logged_in}")
    
    # Simplified routing to ensure login page is shown if conditions for other pages aren't met
    if st.session_state.get('logged_in'): # Use .get for safety
        print("DEBUG_MAIN_APP: Routing to CHAT page.")
        display_chat_app_page()
    elif st.session_state.get('page') == "register":
        print("DEBUG_MAIN_APP: Routing to REGISTER page.")
        display_register_page()
    else: # Default to login
        print("DEBUG_MAIN_APP: Defaulting/Routing to LOGIN page.")
        st.session_state.page = "login" # Ensure it's set
        display_login_page()

if __name__ == "__main__":
    main()