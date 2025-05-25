import streamlit as st
import os
import html
from streamlit_chat import message 
import json 
import traceback 

# For password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# --- Firebase Initialization ---
app_id_global = 'default-app-id-local-dev' 
db = None 

if '__app_id' in globals():
    app_id_global = globals()['__app_id']
    print(f"CANVAS_ENV: Using provided __app_id: {app_id_global}")

try:
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

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if not firebase_admin._apps:
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                cred = credentials.ApplicationDefault(); firebase_admin.initialize_app(cred); db = firestore.client()
                print("SUCCESS: Firebase Admin SDK initialized via GOOGLE_APPLICATION_CREDENTIALS.")
            elif '__firebase_config' in globals() and globals()['__firebase_config']:
                print("INFO: Found __firebase_config. Attempting default init for Admin SDK (may fail).")
                try:
                    cred = credentials.ApplicationDefault(); firebase_admin.initialize_app(cred); db = firestore.client()
                    print("SUCCESS: Firebase Admin SDK initialized using Application Default (after finding __firebase_config).")
                except Exception as default_cred_error:
                    print(f"WARN: Default credentials failed after finding __firebase_config ({default_cred_error}). Using MOCK DB.")
                    raise EnvironmentError("No Firebase Admin credentials for SDK.")
            else: 
                print("INFO: No Firebase Admin credentials. Using MOCK Firestore database.")
                raise EnvironmentError("No Firebase credentials found for Admin SDK.")
        else:
            db = firestore.client(); print("INFO: Firebase Admin SDK already initialized.")
    except (ImportError, EnvironmentError, Exception) as e: 
        print(f"WARN: Could not initialize Firebase Admin SDK ({type(e).__name__}: {e}). Using MOCK Firestore database.")
        class MockDB: 
            def collection(self, collection_name): 
                print(f"MOCK_DB: Accessing collection '{collection_name}'")
                return MockFirestoreCollection()
        db = MockDB() 
except Exception as e: 
    print(f"CRITICAL_ERROR: Outer Firebase/Mock initialization block failed: {e}. Application might not work correctly."); traceback.print_exc()
    if db is None: 
        print("EMERGENCY_FALLBACK: Using MOCK Firestore database due to critical outer error.")
        class MockDB: 
            def collection(self, collection_name): return MockFirestoreCollection()
        db = MockDB()

USER_CREDENTIALS_COLLECTION = f"artifacts/{app_id_global}/user_auth_credentials"

try:
    from gemini_handler import get_gemini_response
    EDI_SPEC_DETAILS_MAP = { 
        "DELFOR_D04A": {"display": "DELFOR D04A", "standard": "EDIFACT", "message_type": "DELFOR", "version": "D04A"},
        "DELFOR_D96A": {"display": "DELFOR D96A", "standard": "EDIFACT", "message_type": "DELFOR", "version": "D96A"},
        "DESADV_D07A": {"display": "DESADV D07A", "standard": "EDIFACT", "message_type": "DESADV", "version": "D07A"},
        "DESADV_D96A": {"display": "DESADV D96A", "standard": "EDIFACT", "message_type": "DESADV", "version": "D96A"},
    }
    LOCAL_SPEC_OPTIONS_MAP = {"Select a Specification...": None}
    for key, details in EDI_SPEC_DETAILS_MAP.items(): LOCAL_SPEC_OPTIONS_MAP[details["display"]] = key
except ImportError:
    print("WARNING: 'gemini_handler.py' not found."); LOCAL_SPEC_OPTIONS_MAP = {"Select a Specification...": None}; EDI_SPEC_DETAILS_MAP = {} 
    def get_gemini_response(user_input, spec_option=None, use_gemini_model=True, spec_details=None): return f"(Placeholder) Response to: '{html.escape(user_input)}'"

def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else: print(f"Warning: CSS file not found at {file_path}")

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
    with st.form("login_form_v3_debug"): 
        email = st.text_input("Email", key="login_email_v3_debug")
        password = st.text_input("Password", type="password", key="login_password_v3_debug")
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
    if st.button("Don't have an account? Register here.", key="goto_register_btn_v3_debug"):
        print("DEBUG_MAIN_APP: 'Register here' button CLICKED.") 
        st.session_state.page = "register"; st.rerun()
    print("DEBUG_MAIN_APP: 'Register here' button rendering attempted.") 
    print("DEBUG_MAIN_APP: >>> display_login_page() FINISHED <<<") 


def display_register_page():
    print("DEBUG_MAIN_APP: >>> display_register_page() CALLED <<<") 
    st.subheader("Register New Account")
    with st.form("register_form_v3_debug"): 
        email = st.text_input("Email", key="register_email_v3_debug")
        password = st.text_input("Password", type="password", key="register_password_v3_debug")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_v3_debug")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            if not email or not password or not confirm_password: st.error("Please fill in all fields.")
            elif password != confirm_password: st.error("Passwords do not match.")
            else:
                success, message_text = register_user(email, password)
                if success: st.success(message_text); st.session_state.page = "login"; st.rerun()
                else: st.error(message_text)
    if st.button("Already have an account? Login here.", key="goto_login_btn_v3_debug"):
        st.session_state.page = "login"; st.rerun()
    print("DEBUG_MAIN_APP: >>> display_register_page() FINISHED <<<") 


def display_chat_app_page():
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() CALLED <<<") 
    SELECTED_SPEC_KEY_STATE = "selected_spec_internal_key" 
    
    username_display = "User" 
    if st.session_state.get("user_email"):
        username_display = st.session_state.user_email.split('@')[0]
    st.sidebar.subheader(f"Welcome, {username_display}!")

    if st.sidebar.button("Logout", key="logout_btn_chat_v3_debug"):
        st.session_state.logged_in = False; st.session_state.user_email = None; st.session_state.page = "login"
        if "messages" in st.session_state: del st.session_state.messages
        if SELECTED_SPEC_KEY_STATE in st.session_state: del st.session_state[SELECTED_SPEC_KEY_STATE]
        st.rerun()

    st.markdown("""<div class="app-header"><h1>Volvo Cars EDI AI Assistant</h1><p>AI Assistant for Suppliers of Volvo Cars EDI</p></div>""", unsafe_allow_html=True)
    if "use_ai_model" not in st.session_state: st.session_state.use_ai_model = True
    if SELECTED_SPEC_KEY_STATE not in st.session_state: st.session_state[SELECTED_SPEC_KEY_STATE] = None
    col1_toggle, col_toggle_main, col3_toggle = st.columns([0.2, 0.6, 0.2])
    with col_toggle_main:
        ai_model_toggled_on = st.toggle("Use AI Model (Gemini)", value=st.session_state.use_ai_model, key="ai_model_toggle_chat_v3_debug", help="Toggle ON for AI responses. Toggle OFF for local data lookup.")
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
            selected_display_option = st.selectbox("Select EDI Specification for Local Data:", options=display_options_list, index=display_options_list.index(current_display_value_for_selectbox), key="local_spec_selector_chat_v3_debug")
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
        # --- FEEDBACK UI REMOVED ---
        # if "feedbacks" not in st.session_state: st.session_state.feedbacks = {} 
        for i, msg_data in enumerate(st.session_state.messages):
            message(msg_data["content"], is_user=(msg_data["role"] == "user"), key=f"msg_chat_display_v3_debug_{i}", avatar_style="initials" if msg_data["role"] == "user" else "bottts", seed="User" if msg_data["role"] == "user" else "AI")
            # --- FEEDBACK UI RENDERING LOGIC REMOVED ---
            # if msg_data["role"] == "assistant" and ... :
            #    ... (feedback button code was here) ...
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sticky-input-area">', unsafe_allow_html=True)
    # The clear_on_submit=True should handle clearing the input after form submission + rerun
    with st.form("user_input_form_chat_v3_debug", clear_on_submit=True): 
        user_input_value = st.text_input("Ask me anything!", key="user_input_widget_chat_v3_debug", placeholder="Ask me anything!", label_visibility="collapsed")
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
        st.rerun() # This is key for clear_on_submit to work and UI to update
    print("DEBUG_MAIN_APP: >>> display_chat_app_page() FINISHED <<<")


def main():
    st.set_page_config(layout="centered", page_title="Volvo Cars EDI AI Assistant")
    # Keep CSS loading enabled unless specifically debugging CSS issues
    load_css(os.path.join("assets", "style.css"))
    # print("DEBUG_MAIN_APP: CSS loading is SKIPPED for this test.") # Keep this commented out for normal operation


    if "page" not in st.session_state:
        print("DEBUG_MAIN_APP: Initializing 'page' to 'login'")
        st.session_state.page = "login"
    if "logged_in" not in st.session_state:
        print("DEBUG_MAIN_APP: Initializing 'logged_in' to False")
        st.session_state.logged_in = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None 
    
    print(f"DEBUG_MAIN_APP: In main() - Current page: '{st.session_state.page}', Logged in: {st.session_state.logged_in}")
    
    if st.session_state.logged_in:
        print("DEBUG_MAIN_APP: User is logged in. Routing to CHAT page.")
        display_chat_app_page()
    elif st.session_state.page == "register":
        print("DEBUG_MAIN_APP: Page is 'register'. Routing to REGISTER page.")
        display_register_page()
    else: 
        print("DEBUG_MAIN_APP: Not logged in and page is not 'register'. Forcing LOGIN page display.")
        st.session_state.page = "login" 
        display_login_page()

if __name__ == "__main__":
    main()
