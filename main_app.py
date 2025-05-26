import streamlit as st
import os
import html
from streamlit_chat import message 
import json 
import traceback 

# For password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# --- Session State Initialization for Mock DB ---
if "_mock_db_users_store" not in st.session_state:
    st.session_state._mock_db_users_store = {}
    print(f"INFO: Initializing MOCK Firestore IN SESSION_STATE. Initial store: {st.session_state._mock_db_users_store}")

# --- Firebase Initialization (Simplified to MOCK for this UI test) ---
app_id_global = 'default-app-id-local-dev' 
db = None 
print(f"INFO: Using app_id_global: {app_id_global}")


class MockFirestoreDocument:
    def __init__(self, doc_id, data=None):
        self.id = doc_id
        self._data = data if data is not None else {}
        self._exists = data is not None 
        # print(f"MOCK_DOC_INIT: ID='{self.id}', Data='{self._data}', Exists={self._exists}") # Can be noisy

    def get(self): 
        # print(f"MOCK_DOC_GET: ID='{self.id}', Exists={self.exists}")
        return self 
    
    def to_dict(self):
        return self._data
    
    @property 
    def exists(self): 
        return self._exists
    
    def set(self, data_to_set):
        # Access mock store from session_state
        if self.id:
            st.session_state._mock_db_users_store[self.id] = data_to_set
            self._data = data_to_set
            self._exists = True 
            print(f"MOCK_DB_SET (Session): User '{self.id}', Data: {data_to_set}. Current store: {st.session_state._mock_db_users_store}")
        else:
            print("MOCK_DB_SET_ERROR: Document ID is None, cannot set.")


class MockFirestoreQuery: 
    def __init__(self, field, op, value):
        self._results = []
        # Access mock store from session_state
        # print(f"MOCK_QUERY_INIT: Field='{field}', Op='{op}', Value='{value}', Store='{st.session_state._mock_db_users_store}'")
        if field == "email" and op == "==" and value in st.session_state._mock_db_users_store:
            self._results.append(MockFirestoreDocument(value, st.session_state._mock_db_users_store[value]))
        # print(f"MOCK_QUERY_INIT: Results count: {len(self._results)}")
    def stream(self): return self._results
    def get(self): return self._results

class MockFirestoreCollection:
    def document(self, doc_id=None): 
        # print(f"MOCK_COLLECTION_DOC: Accessing document '{doc_id}'")
        if doc_id:
            # Access mock store from session_state
            return MockFirestoreDocument(doc_id, st.session_state._mock_db_users_store.get(doc_id))
        raise ValueError("Mock document requires an ID for this user collection pattern.")
    def where(self, field, op, value): return MockFirestoreQuery(field, op, value)

class MockDB: 
    def collection(self, collection_name): 
        # print(f"MOCK_DB_ACCESS: Collection '{collection_name}'")
        return MockFirestoreCollection()
db = MockDB() # Initialize our mock DB interface

USER_CREDENTIALS_COLLECTION = f"artifacts/{app_id_global}/user_auth_credentials" # Path for collection (conceptual for mock)

# --- Placeholders for other parts of your app ---
EDI_SPEC_DETAILS_MAP = { 
    "DELFOR_D04A": {"display": "DELFOR D04A", "standard": "EDIFACT", "message_type": "DELFOR", "version": "D04A"},
    "DELFOR_D96A": {"display": "DELFOR D96A", "standard": "EDIFACT", "message_type": "DELFOR", "version": "D96A"},
    "DESADV_D07A": {"display": "DESADV D07A", "standard": "EDIFACT", "message_type": "DESADV", "version": "D07A"},
    "DESADV_D96A": {"display": "DESADV D96A", "standard": "EDIFACT", "message_type": "DESADV", "version": "D96A"},
}
LOCAL_SPEC_OPTIONS_MAP = {"Select a Specification...": None}
for key, details in EDI_SPEC_DETAILS_MAP.items(): LOCAL_SPEC_OPTIONS_MAP[details["display"]] = key

try:
    from gemini_handler import get_gemini_response
except ImportError:
    print("WARNING: 'gemini_handler.py' not found. Using placeholder.")
    def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None):
        return f"(Placeholder) Response to: '{html.escape(user_input)}'"

def load_css(file_path):
    # For this test, ensure CSS is loaded if you have style.css
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        print(f"Warning: CSS file not found at {file_path}")


def register_user(email, password):
    print(f"DEBUG_REGISTER: Attempting to register email: '{email}'")
    if not db: 
        st.error("Database service is not available (register_user)."); 
        return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        user_doc_snapshot = user_doc_ref 
        print(f"DEBUG_REGISTER: Checking for existing user '{email}'. Snapshot Exists: {user_doc_snapshot.exists}")
        if user_doc_snapshot.exists: 
            print(f"DEBUG_REGISTER: Email '{email}' already exists.")
            return False, "Email already registered."
        
        hashed_password = generate_password_hash(password)
        user_doc_ref.set({"email": email, "hashed_password": hashed_password}) 
        print(f"DEBUG_REGISTER: Registration successful for '{email}'.")
        return True, "Registration successful! Please login."
    except Exception as e: 
        print(f"ERROR_REGISTER: {e}"); traceback.print_exc()
        return False, f"Registration failed: An unexpected error occurred."

def login_user(email, password):
    print(f"DEBUG_LOGIN: Attempting to login email: '{email}'")
    if not db: 
        st.error("Database service is not available (login_user)."); 
        return False, "Database service not available."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        user_doc_snapshot = user_doc_ref 
        print(f"DEBUG_LOGIN: Checked for user '{email}'. Snapshot Exists: {user_doc_snapshot.exists}")
        if user_doc_snapshot.exists: 
            user_data = user_doc_snapshot.to_dict()
            print(f"DEBUG_LOGIN: User data for '{email}': {user_data}")
            if user_data and check_password_hash(user_data.get("hashed_password", ""), password):
                print(f"DEBUG_LOGIN: Password MATCH for '{email}'")
                return True, "Login successful!"
            print(f"DEBUG_LOGIN: Password MISMATCH for '{email}'")
            return False, "Incorrect password."
        print(f"DEBUG_LOGIN: Email '{email}' not found in store: {st.session_state._mock_db_users_store}")
        return False, "Email not found."
    except Exception as e: 
        print(f"ERROR_LOGIN: {e}"); traceback.print_exc()
        return False, f"Login failed: An unexpected error occurred."

def display_login_page():
    print("DEBUG_MAIN_APP: >>> display_login_page() CALLED <<<") 
    
    # Moved Register button to the VERY TOP to ensure it renders
    print("DEBUG_MAIN_APP: Rendering 'Register here' button FIRST.") 
    if st.button("Don't have an account? Register here.", key="goto_register_btn_session_debug"):
        print("DEBUG_MAIN_APP: 'Register here' (top) button CLICKED.") 
        st.session_state.page = "register"
        st.rerun()
    print("DEBUG_MAIN_APP: 'Register here' (top) button rendering attempted.") 
    
    st.subheader("Login")
    with st.form("login_form_session_debug"): 
        email = st.text_input("Email", key="login_email_session_debug")
        password = st.text_input("Password", type="password", key="login_password_session_debug")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            print(f"DEBUG_LOGIN_FORM: Login form submitted with email: {email}")
            if not email or not password: st.error("Please enter both email and password.")
            else:
                success, message_text = login_user(email, password)
                if success:
                    st.session_state.logged_in = True; st.session_state.user_email = email; st.session_state.page = "chat" 
                    st.success(message_text); st.rerun() 
                else: st.error(message_text)
    print("DEBUG_MAIN_APP: >>> display_login_page() FINISHED <<<") 

def display_register_page():
    print("DEBUG_MAIN_APP: >>> display_register_page() CALLED <<<") 
    st.subheader("Register New Account")
    with st.form("register_form_session_debug"): 
        email = st.text_input("Email", key="register_email_session_debug")
        password = st.text_input("Password", type="password", key="register_password_session_debug")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_session_debug")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            print(f"DEBUG_REGISTER_FORM: Register form submitted with email: {email}")
            if not email or not password or not confirm_password: st.error("Please fill in all fields.")
            elif password != confirm_password: st.error("Passwords do not match.")
            else:
                success, message_text = register_user(email, password)
                if success: st.success(message_text); st.session_state.page = "login"; st.rerun()
                else: st.error(message_text)
    if st.button("Already have an account? Login here.", key="goto_login_btn_session_debug"):
        st.session_state.page = "login"; st.rerun()
    print("DEBUG_MAIN_APP: >>> display_register_page() FINISHED <<<") 

def display_chat_app_page(): 
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() CALLED <<<") 
    SELECTED_SPEC_KEY_STATE = "selected_spec_internal_key" # Define it here or pass as arg
    
    username_display = "User" 
    if st.session_state.get("user_email"):
        try: username_display = st.session_state.user_email.split('@')[0]
        except: pass 
    st.sidebar.subheader(f"Welcome, {username_display}!")

    if st.sidebar.button("Logout", key="logout_chat_session_debug"):
        st.session_state.logged_in = False; st.session_state.user_email = None; st.session_state.page = "login"
        if "messages" in st.session_state: del st.session_state.messages # Clear chat history on logout
        if SELECTED_SPEC_KEY_STATE in st.session_state: del st.session_state[SELECTED_SPEC_KEY_STATE]
        st.rerun()

    # --- Main Chat Interface (Copied from your previous full version) ---
    st.markdown("""<div class="app-header"><h1>Volvo Cars EDI AI Assistant</h1><p>AI Assistant for Suppliers of Volvo Cars EDI</p></div>""", unsafe_allow_html=True)
    if "use_ai_model" not in st.session_state: st.session_state.use_ai_model = True
    if SELECTED_SPEC_KEY_STATE not in st.session_state: st.session_state[SELECTED_SPEC_KEY_STATE] = None
    
    col1_toggle, col_toggle_main, col3_toggle = st.columns([0.2, 0.6, 0.2])
    with col_toggle_main:
        ai_model_toggled_on = st.toggle("Use AI Model (Gemini)", value=st.session_state.use_ai_model, key="ai_model_toggle_chat_session", help="Toggle ON for AI responses. Toggle OFF for local data lookup.")
        if ai_model_toggled_on != st.session_state.use_ai_model:
            st.session_state.use_ai_model = ai_model_toggled_on; st.rerun()
    
    current_selected_spec_details_for_handler = None 
    if not st.session_state.use_ai_model:
        col1_select, col_select_main, col3_select = st.columns([0.1, 0.8, 0.1])
        with col_select_main:
            display_options_list = list(LOCAL_SPEC_OPTIONS_MAP.keys())
            current_display_value_for_selectbox = "Select a Specification..."
            stored_key = st.session_state.get(SELECTED_SPEC_KEY_STATE)
            if stored_key and stored_key in EDI_SPEC_DETAILS_MAP:
                current_display_value_for_selectbox = EDI_SPEC_DETAILS_MAP[stored_key]["display"]
            selected_display_option = st.selectbox("Select EDI Specification for Local Data:", options=display_options_list, index=display_options_list.index(current_display_value_for_selectbox), key="local_spec_selector_chat_session")
            newly_selected_key = LOCAL_SPEC_OPTIONS_MAP[selected_display_option]
            if newly_selected_key != st.session_state.get(SELECTED_SPEC_KEY_STATE):
                st.session_state[SELECTED_SPEC_KEY_STATE] = newly_selected_key
                if newly_selected_key and newly_selected_key in EDI_SPEC_DETAILS_MAP: 
                    current_selected_spec_details_for_handler = EDI_SPEC_DETAILS_MAP[newly_selected_key]
                    if "messages" not in st.session_state: st.session_state.messages = []
                    st.session_state.messages.append({"role": "user", "content": f"Show information for {current_selected_spec_details_for_handler['display']}"})
                st.rerun() 
            if st.session_state.get(SELECTED_SPEC_KEY_STATE) and st.session_state[SELECTED_SPEC_KEY_STATE] in EDI_SPEC_DETAILS_MAP:
                 current_selected_spec_details_for_handler = EDI_SPEC_DETAILS_MAP.get(st.session_state[SELECTED_SPEC_KEY_STATE])
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<div class="chat-messages-area" id="chat-messages-area-streamlit-chat">', unsafe_allow_html=True)
    with st.container(): 
        if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm the EDI AI Assistant for Volvo Cars."},{"role": "assistant", "content": "How can I help you today?"}]
        for i, msg_data in enumerate(st.session_state.messages):
            message(msg_data["content"], is_user=(msg_data["role"] == "user"), key=f"msg_chat_display_session_{i}", avatar_style="initials" if msg_data["role"] == "user" else "bottts", seed="User" if msg_data["role"] == "user" else "AI")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sticky-input-area">', unsafe_allow_html=True)
    with st.form("user_input_form_chat_session", clear_on_submit=True): 
        user_input_value = st.text_input("Ask me anything!", key="user_input_widget_chat_session", placeholder="Ask me anything!", label_visibility="collapsed")
        submitted = st.form_submit_button("✈️") 
    with st.container(): 
        st.markdown("""<div class="footer-text"><p>Volvo Cars EDI AI Assistant provides AI-generated responses. Please verify important information.</p><p>© Copyright AB Volvo 2025 &nbsp;|&nbsp;<a href="#">Privacy</a> &nbsp;|&nbsp;<a href="https://www.volvocars.com">www.volvocars.com</a></p></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted and user_input_value:
        if "messages" not in st.session_state: st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": user_input_value})
        spec_option_key_to_pass = None; final_spec_details_for_handler = None 
        current_selected_key = st.session_state.get(SELECTED_SPEC_KEY_STATE)
        if current_selected_key and current_selected_key in EDI_SPEC_DETAILS_MAP: 
            spec_option_key_to_pass = current_selected_key
            final_spec_details_for_handler = EDI_SPEC_DETAILS_MAP.get(spec_option_key_to_pass)
        if not st.session_state.use_ai_model and not final_spec_details_for_handler: 
             spec_option_key_to_pass = None 
        print(f"[MAIN_APP DEBUG] Passing to handler: user_input='{user_input_value}', spec_option_key='{spec_option_key_to_pass}', spec_details='{final_spec_details_for_handler}', use_ai_model={st.session_state.use_ai_model}")
        assistant_response = get_gemini_response(user_input_value, spec_option=spec_option_key_to_pass, use_gemini_model=st.session_state.use_ai_model, spec_details=final_spec_details_for_handler)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.rerun()
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() FINISHED <<<") 

def main():
    st.set_page_config(layout="centered", page_title="Volvo Cars EDI AI Assistant - Auth Debug v3")
    load_css(os.path.join("assets", "style.css")) # Re-enable CSS loading

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
    
    if st.session_state.get('logged_in'): 
        print("DEBUG_MAIN_APP: Routing to CHAT page.")
        display_chat_app_page()
    elif st.session_state.get('page') == "register":
        print("DEBUG_MAIN_APP: Routing to REGISTER page.")
        display_register_page()
    else: 
        print("DEBUG_MAIN_APP: Defaulting/Routing to LOGIN page.")
        st.session_state.page = "login" 
        display_login_page()

if __name__ == "__main__":
    main()