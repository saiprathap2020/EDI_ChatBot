import streamlit as st
import os
import html
from streamlit_chat import message 
import json 
import traceback 

# For password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# --- Session State Initialization for Mock DB & App State ---
if "_mock_db_users_store_session_data" not in st.session_state:
    st.session_state._mock_db_users_store_session_data = {}
    print(f"INFO: Initializing MOCK Firestore store IN SESSION_STATE. Initial store: {st.session_state._mock_db_users_store_session_data}")

if "page" not in st.session_state:
    st.session_state.page = "login" 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- Firebase Initialization ---
app_id_global = 'default-app-id-local-dev' 
db = None 
IS_MOCK_DB = True # Assume mock until real Firebase initializes successfully

print(f"--- SCRIPT START (Auth Debug v6) ---")
if '__app_id' in globals(): app_id_global = globals()['__app_id']

USER_CREDENTIALS_COLLECTION = f"artifacts/{app_id_global}/user_auth_credentials_debug_v2" # Using a distinct collection for clarity

class MockFirestoreDocument:
    def __init__(self, doc_id, data=None):
        self.id = doc_id; self._data = data if data is not None else {}; self._exists = data is not None
    def get(self): return self 
    def to_dict(self): return self._data
    @property 
    def exists(self): return self._exists
    def set(self, data_to_set):
        if self.id:
            st.session_state._mock_db_users_store_session_data[self.id] = data_to_set 
            self._data = data_to_set; self._exists = True
            print(f"MOCK_DB_SET (Session): User '{self.id}'. Store: {st.session_state._mock_db_users_store_session_data}")
        else: print("MOCK_DB_SET_ERROR: Document ID is None.")

class MockFirestoreQuery: 
    def __init__(self, field, op, value):
        self._results = []
        if field == "email" and op == "==" and value in st.session_state._mock_db_users_store_session_data:
            self._results.append(MockFirestoreDocument(value, st.session_state._mock_db_users_store_session_data[value]))
    def stream(self): return self._results; 
    def get(self): return self._results

class MockFirestoreCollection:
    def document(self, doc_id=None): 
        if doc_id: return MockFirestoreDocument(doc_id, st.session_state._mock_db_users_store_session_data.get(doc_id))
        raise ValueError("Mock document requires an ID for user collection.")
    def where(self, field, op, value): return MockFirestoreQuery(field, op, value)

class MockDB: 
    def collection(self, collection_name): 
        print(f"MOCK_DB_ACCESS: Using MockDB for collection '{collection_name}'")
        return MockFirestoreCollection()

# --- Firebase Admin SDK Initialization Logic ---
try:
    print("FIREBASE_INIT: Attempting to initialize Firebase Admin SDK...")
    google_app_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    streamlit_secret_firebase_json = st.secrets.get("FIREBASE_SERVICE_ACCOUNT_JSON_CONTENT") if "FIREBASE_SERVICE_ACCOUNT_JSON_CONTENT" in st.secrets else None

    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred = None
        if google_app_creds:
            print(f"FIREBASE_INIT: Found GOOGLE_APPLICATION_CREDENTIALS env var: {google_app_creds}")
            try:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                IS_MOCK_DB = False
                print("SUCCESS: Firebase Admin SDK initialized using GOOGLE_APPLICATION_CREDENTIALS.")
            except Exception as e_gac:
                print(f"WARN: Failed to init Firebase from GOOGLE_APPLICATION_CREDENTIALS: {e_gac}. Will try secrets or mock.")
                db = None # Ensure db is reset if GAC init fails
        
        if db is None and streamlit_secret_firebase_json: # If GAC failed or not set, try Streamlit Secret
            print("FIREBASE_INIT: GOOGLE_APPLICATION_CREDENTIALS failed or not set. Trying Streamlit Secret FIREBASE_SERVICE_ACCOUNT_JSON_CONTENT.")
            try:
                cred_dict = json.loads(streamlit_secret_firebase_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred) # This might error if already initialized by failed GAC
                db = firestore.client()
                IS_MOCK_DB = False
                print("SUCCESS: Firebase Admin SDK initialized from Streamlit Secret.")
            except Exception as e_streamlit_secret:
                print(f"WARN: Failed to init Firebase from Streamlit JSON secret: {e_streamlit_secret}. Using MOCK DB.")
                db = MockDB(); IS_MOCK_DB = True # Explicitly use MockDB
        elif db is None: # If neither GAC nor Streamlit Secret worked
             print("INFO: No valid REAL Firebase Admin credentials found (env var or Streamlit Secret). Using MOCK Firestore.")
             db = MockDB(); IS_MOCK_DB = True
    else: # Firebase app already initialized
        db = firestore.client(); IS_MOCK_DB = False
        print("INFO: Firebase Admin SDK already initialized (Real Firestore).")

except (ImportError, Exception) as e: # Catch issues like firebase_admin not installed
    print(f"WARN: Could not initialize REAL Firebase Admin SDK or an error occurred ({type(e).__name__}: {e}). Using MOCK Firestore database.")
    db = MockDB(); IS_MOCK_DB = True

print(f"DB_STATUS: Using {'MockDB (persists in session)' if IS_MOCK_DB else 'Real Firestore'}. Collection path: {USER_CREDENTIALS_COLLECTION}")


# --- Gemini Handler (Placeholder) & EDI Maps ---
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
    print(f"AUTH_FUNC_REGISTER: Attempting for '{email}' using {'MockDB' if IS_MOCK_DB else 'Real Firestore'}")
    if not db: st.error("Database service is not available."); return False, "Database error."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        doc_snapshot = user_doc_ref.get() if not IS_MOCK_DB else user_doc_ref 
        print(f"AUTH_FUNC_REGISTER: User '{email}' exists check: {doc_snapshot.exists}")
        if doc_snapshot.exists: return False, "Email already registered."
        user_doc_ref.set({"email": email, "hashed_password": generate_password_hash(password)})
        return True, "Registration successful! Please login."
    except Exception as e: print(f"ERROR_REGISTER: {e}"); traceback.print_exc(); return False, f"Registration error."

def login_user(email, password):
    print(f"AUTH_FUNC_LOGIN: Attempting for '{email}' using {'MockDB' if IS_MOCK_DB else 'Real Firestore'}")
    if not db: st.error("Database service is not available."); return False, "Database error."
    try:
        user_doc_ref = db.collection(USER_CREDENTIALS_COLLECTION).document(email)
        doc_snapshot = user_doc_ref.get() if not IS_MOCK_DB else user_doc_ref
        print(f"AUTH_FUNC_LOGIN: User '{email}' exists check: {doc_snapshot.exists}")
        if doc_snapshot.exists:
            user_data = doc_snapshot.to_dict()
            if user_data and check_password_hash(user_data.get("hashed_password", ""), password):
                print(f"AUTH_FUNC_LOGIN: Password match for '{email}'.")
                return True, "Login successful!"
            print(f"AUTH_FUNC_LOGIN: Password mismatch for '{email}'.")
            return False, "Incorrect password."
        print(f"AUTH_FUNC_LOGIN: Email '{email}' not found. Mock store: {st.session_state._mock_db_users_store_session_data if IS_MOCK_DB else 'N/A'}")
        return False, "Email not found."
    except Exception as e: print(f"ERROR_LOGIN: {e}"); traceback.print_exc(); return False, f"Login error."

def display_login_page():
    print("PAGE_RENDER: display_login_page()")
    if st.button("Don't have an account? Register here.", key="goto_register_btn_main_v6"):
        st.session_state.page = "register"; st.rerun()
    st.subheader("Login")
    with st.form("login_form_main_v6"): 
        email = st.text_input("Email", key="login_email_main_v6")
        password = st.text_input("Password", type="password", key="login_password_main_v6")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            success, message_text = login_user(email, password)
            if success:
                st.session_state.logged_in = True; st.session_state.user_email = email; st.session_state.page = "chat" 
                st.rerun() 
            else: st.error(message_text)

def display_register_page():
    print("PAGE_RENDER: display_register_page()")
    st.subheader("Register New Account")
    with st.form("register_form_main_v6"): 
        email = st.text_input("Email", key="register_email_main_v6")
        password = st.text_input("Password", type="password", key="register_password_main_v6")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_main_v6")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            if not email or not password or not confirm_password: st.error("Please fill all fields.")
            elif password != confirm_password: st.error("Passwords do not match.")
            else:
                success, message_text = register_user(email, password)
                if success: st.success(message_text); st.session_state.page = "login"; st.rerun()
                else: st.error(message_text)
    if st.button("Already have an account? Login here.", key="goto_login_btn_main_v6"):
        st.session_state.page = "login"; st.rerun()

def display_chat_app_page(): 
    print("PAGE_RENDER: display_chat_app_page()")
    SELECTED_SPEC_KEY_STATE = "selected_spec_internal_key_v6" 
    st.sidebar.subheader(f"Welcome, {st.session_state.get('user_email', 'User').split('@')[0]}!")
    if st.sidebar.button("Logout", key="logout_chat_main_v6"):
        st.session_state.logged_in = False; st.session_state.user_email = None; st.session_state.page = "login"
        if "messages" in st.session_state: del st.session_state.messages 
        if SELECTED_SPEC_KEY_STATE in st.session_state: del st.session_state[SELECTED_SPEC_KEY_STATE]
        st.rerun()
    # ... (Rest of chat page UI: header, toggle, selectbox, messages, input form, footer from previous "Full Version") ...
    st.markdown("""<div class="app-header"><h1>Volvo Cars EDI AI Assistant</h1><p>AI Assistant for Suppliers of Volvo Cars EDI</p></div>""", unsafe_allow_html=True)
    if "use_ai_model" not in st.session_state: st.session_state.use_ai_model = True
    if SELECTED_SPEC_KEY_STATE not in st.session_state: st.session_state[SELECTED_SPEC_KEY_STATE] = None
    st.sidebar.markdown("---") 
    st.session_state.use_ai_model = st.sidebar.toggle("Use AI Model (Gemini)", value=st.session_state.use_ai_model, key="ai_model_toggle_sidebar_v2_final_v6", help="Toggle ON for AI responses. Toggle OFF for local data lookup.")
    current_selected_spec_details_for_handler = None 
    if not st.session_state.use_ai_model:
        display_options_list = list(LOCAL_SPEC_OPTIONS_MAP.keys())
        current_display_value_for_selectbox = "Select a Specification..."
        stored_key = st.session_state.get(SELECTED_SPEC_KEY_STATE)
        if stored_key and stored_key in EDI_SPEC_DETAILS_MAP: current_display_value_for_selectbox = EDI_SPEC_DETAILS_MAP[stored_key]["display"]
        selected_display_option = st.sidebar.selectbox("Select EDI Specification:", options=display_options_list, index=display_options_list.index(current_display_value_for_selectbox), key="local_spec_selector_sidebar_v2_final_v6")
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
            message(msg_data["content"], is_user=(msg_data["role"] == "user"), key=f"msg_chat_display_session_v2_final_v6_{i}", avatar_style="initials" if msg_data["role"] == "user" else "bottts", seed="User" if msg_data["role"] == "user" else "AI")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sticky-input-area">', unsafe_allow_html=True)
    with st.form("user_input_form_chat_session_v2_final_v6", clear_on_submit=True): 
        user_input_value = st.text_input("Ask me anything!", key="user_input_widget_chat_session_v2_final_v6", placeholder="Ask me anything!", label_visibility="collapsed")
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

def main():
    st.set_page_config(layout="centered", page_title="Volvo Cars EDI AI Assistant - Auth Debug v6")
    load_css(os.path.join("assets", "style.css")) 

    if "page" not in st.session_state: st.session_state.page = "login" 
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "user_email" not in st.session_state: st.session_state.user_email = None
    
    print(f"DEBUG_MAIN_APP: In main() - Current page: '{st.session_state.page}', Logged in: {st.session_state.logged_in}, DB is MOCK: {IS_MOCK_DB}")
    
    if st.session_state.get('logged_in'): display_chat_app_page()
    elif st.session_state.get('page') == "register": display_register_page()
    else: st.session_state.page = "login"; display_login_page()

if __name__ == "__main__":
    main()
