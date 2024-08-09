import bcrypt
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai
import os
import ipdb

def hash_pwd(pwd):
    pwd = pwd.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed.decode()

def check_hash(password, hashed):
    hashed = hashed.encode()
    password = password.encode()
    return bcrypt.checkpw(password, hashed)

def handle_file(uploaded_file):
    """Extract text from uploaded file (PDF, TXT, DOCX)."""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type!")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(txt_file):
    """Extract text from a TXT file."""
    return txt_file.read().decode("utf-8")

def extract_text_from_docx(docx_file):
    """Extract text from a DOCX file."""
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def convert_to_dict_format(data):
    """Convert a list of [role, content] into a list of dictionaries with 'role' and 'content' keys."""
    result = []

    for role, content in data:
        role_name = "assistant" if role == 0 else "user"
        result.append({"role": role_name, "content": content})

    return result

def convert_to_history(data):
    """Convert a list of dictionaries with 'role' and 'content' keys into a list of [role, content]."""
    result = "This is the history of our chat:\n"

    for item in data:
        if item[0] == 0:
            result += f"assistant: {item[1]}\n"
        else:
            result += f"user: {item[1]}\n"

    return result

gemini_key = os.environ["token"]

class Gen_chat():
    def __init__(self):
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        self.model = model

    def start_chat(self, history=[]):
        return self.model.start_chat(history=history)

