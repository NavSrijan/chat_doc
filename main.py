import streamlit as st
from functions import check_hash, hash_pwd, handle_file, convert_to_dict_format, Gen_chat, convert_to_history
from db import Users, Messages, Chats, Attachments
import ipdb

genai = Gen_chat()
file_sent = False

if "files_used" not in st.session_state:
    st.session_state.files_used = []

if "users" not in st.session_state:
    st.session_state.users = Users()
if "messages" not in st.session_state:
    st.session_state.messages_obj = Messages()
if "chats" not in st.session_state:
    st.session_state.chats = Chats()
if "attachments" not in st.session_state:
    st.session_state.attachments = Attachments()
if "gen_chat" not in st.session_state:
    st.session_state.gen_chat = Gen_chat()

if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "username" not in st.session_state:
    st.session_state.username = ""
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = st.session_state.chats.get_last_chat(st.session_state.user_id)
    history = convert_to_history(st.session_state.messages_obj.get_messages(st.session_state.selected_chat))
    st.session_state.ai_chat = genai.start_chat()
    st.session_state.ai_chat.send_message(history)

def check_password():
    """Returns `True` if the user has a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)
    
    def register_form():
        """Form with widgets to collect user information"""
        with st.form("Register"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Register", on_click=register_user)

    def register_user():
        username = st.session_state["username"]
        password = st.session_state["password"]
        pwd_hash = hash_pwd(password)
        st.session_state.users.add_user(username, pwd_hash)
        st.success("Registration successful! You can now log in.")

    def password_entered():
        """Checks whether the entered password is correct."""
        username = st.session_state["username"]
        password = st.session_state["password"]
        pwd_hash = st.session_state.users.get_hash(username)
        if check_hash(password, pwd_hash):
            st.session_state["password_correct"] = True
            st.session_state.user_id = st.session_state.users.get_user_id(username)
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        if "selected_chat" not in st.session_state or st.session_state.selected_chat==1:
            st.session_state.selected_chat = st.session_state.chats.get_last_chat(st.session_state.user_id)
            history = convert_to_history(st.session_state.messages_obj.get_messages(st.session_state.selected_chat))
            st.session_state.ai_chat = genai.start_chat()
            st.session_state.ai_chat.send_message(history)
        return True

    # Show inputs for username + password.
    option = st.selectbox("Select an option", ["Login", "Register"])

    if option == "Login":
        login_form()
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 User not known or password incorrect")
            return False

    elif option == "Register":
        register_form()

def get_chat_messages(chat_id):
    messages = st.session_state.messages_obj.get_messages(chat_id)
    if messages:
        return convert_to_dict_format(messages)
    return [
        {"role": "assistant", "content": "Hello! How can I help you today?"},
        {"role": "assistant", "content": "Send a message before uploading a file."},
    ]

def get_chat_ids(user_id, limit=3):
    return st.session_state.chats.get_chats(user_id, limit=limit) or [st.session_state.chats.add_chat(user_id)]

def get_response(prompt):
    response = st.session_state.ai_chat.send_message(prompt)
    return response.text

if not check_password():
    st.stop()

st.title("💬 Chat Doc")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

with st.sidebar:
    st.radio(
        "Which chat? 👉",
        key="selected_chat",
        options=get_chat_ids(st.session_state.user_id, limit=3),
    )
    st.button("New Chat", on_click=lambda: st.session_state.chats.add_chat(st.session_state.user_id))
    st.write("Upload a file:")
    uploaded_file = st.file_uploader("", key=f"file_uploader_{st.session_state.selected_chat}", accept_multiple_files=False, type=["pdf", "txt", "docx"], help="Upload a PDF, TXT, or DOCX file.")
    if uploaded_file:
        if uploaded_file not in st.session_state.files_used:
            st.session_state.files_used.append(uploaded_file)
            text = handle_file(uploaded_file)
            response_file = st.session_state.ai_chat.send_message("Understand this text:\n"+text)
            file_sent = True
            # Send attachment to the model.
            st.session_state.attachments.add_attachment(st.session_state.selected_chat, text)
            # Remove the file from the session state.
            uploaded_file = None


st.session_state.messages = get_chat_messages(st.session_state.selected_chat)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input() or file_sent:
    if file_sent:
        msg = response_file.text
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        st.session_state.messages_obj.add_message(msg, 0, st.session_state.selected_chat)
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.session_state.messages_obj.add_message(prompt, st.session_state.user_id, st.session_state.selected_chat)
        msg = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        st.session_state.messages_obj.add_message(msg, 0, st.session_state.selected_chat)


