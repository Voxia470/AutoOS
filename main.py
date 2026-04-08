import os
import openai
import pyttsx3
import PyPDF2
import pandas as pd
import threading
import time
import sqlite3
import requests
import base64
from bs4 import BeautifulSoup
from email.message import EmailMessage
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- AI LOGIC ---
def auto_ai_reply(user_email, email_content):
    # Yahan GPT-4 ya Gemini email ko samajh kar reply likhega
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # Ya gpt-4
        messages=[{"role": "system", "content": "You are a professional executive assistant. Reply to this email professionally."},
                  {"role": "user", "content": email_content}]
    )
    return response.choices[0].message.content

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Ye hamara Luxury Frontend load karega
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/connect-gmail")
async def connect_gmail():
    # Yahan hum Google Login (OAuth) ka link denge
    return {"auth_url": "https://accounts.google.com/o/oauth2/v2/auth..."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 1. Load Settings
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Pehle ADMIN_EMAILS likho (SCOPES se bahar)
ADMIN_EMAILS = ["info.luvahair@gmail.com"] 

# Phir SCOPES shuru karo
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar'
]
# --- MEMORY LOGIC ---
def setup_database():
    conn = sqlite3.connect('autoos_memory.db')
    conn.execute('CREATE TABLE IF NOT EXISTS processed_emails (email_id TEXT PRIMARY KEY, status TEXT)')
    conn.commit()
    conn.close()

def is_processed(email_id):
    conn = sqlite3.connect('autoos_memory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email_id FROM processed_emails WHERE email_id = ?', (email_id,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def mark_done(email_id):
    conn = sqlite3.connect('autoos_memory.db')
    conn.execute('INSERT INTO processed_emails (email_id, status) VALUES (?, ?)', (email_id, 'DONE'))
    conn.commit()
    conn.close()

import sqlite3

# AI ki memory file banana
def setup_memory():
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (sender TEXT, content TEXT, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_daily_summary():
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    # Aaj ki saari activities nikaalo
    c.execute("SELECT action FROM history WHERE timestamp >= date('now')")
    actions = c.fetchall()
    conn.close()
    
    summary = f"Sir, Today's Summary:\n- Processed {len(actions)} emails.\n- Handled tasks like: {set(actions)}"
    return summary

# Memory mein baat save karna
def save_to_memory(sender, content, action):
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (sender, content, action) VALUES (?, ?, ?)", (sender, content, action))
    conn.commit()
    conn.close()

# Shuru mein memory setup karlo
setup_memory()

# --- GMAIL & ACTION LOGIC ---
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def send_whatsapp(message):
    phone_number = "34697731054"
    api_key = "6499851"
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={message}&apikey={api_key}"
    try:
        requests.get(url)
        print("📱 WhatsApp notification sent!")
    except Exception as e:
        print(f"WhatsApp Error: {e}")

import PyPDF2

def get_pdf_text(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

import pandas as pd

def get_excel_data(file_path):
    try:
        # Check karte hain ke CSV hai ya Excel
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Data ko text mein badalte hain taake AI samajh sakay
        summary = df.head(10).to_string() # Pehli 10 lines ka nichod
        return f"File Summary:\n{summary}"
    except Exception as e:
        print(f"Excel Error: {e}")
        return "Could not read the spreadsheet."

def download_attachment(service, msg_id, attachment_id, filename):
    attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
    with open(filename, 'wb') as f:
        f.write(file_data)
    return filename

def send_reply(service, thread_id, original_msg_id, reply_text):
    try:
        message = EmailMessage()
        message.set_content(reply_text)
        original = service.users().messages().get(userId='me', id=original_msg_id).execute()
        to_email = next(h['value'] for h in original['payload']['headers'] if h['name'] == 'From')
        subject = next(h['value'] for h in original['payload']['headers'] if h['name'] == 'Subject')
        
        message['To'] = to_email
        message['Subject'] = f"Re: {subject}"
        message['In-Reply-To'] = original_msg_id
        message['References'] = original_msg_id
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': encoded_message, 'threadId': thread_id}).execute()
        print(f"📧 AI Replied to: {to_email}")
    except Exception as e:
        print(f"Reply Error: {e}")

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    # Awaaz ki speed thodi natural rakhte hain
    engine.setProperty('rate', 170) 
    engine.say(text)
    engine.runAndWait()

# Yahan apni Sheet ID dalo
SPREADSHEET_ID = '1h4bzESAJzPb78H25vV4Ke_i9kwqjoZ7iefS8ukzQRJY'

def log_to_sheet(snippet, decision_status):
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        sheet_service = build('sheets', 'v4', credentials=creds)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        values = [[timestamp, snippet, decision_status]]
        body = {'values': values}
        sheet_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A:C",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print("📊 Logged to Google Sheet Successfully!")
    except Exception as e:
        print(f"Sheets Error: {e}")

def fetch_web_data(query):
    print(f"🔍 Searching the web for: {query}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://www.google.com/search?q={query}", timeout=60000)
            content = page.inner_text('body') 
            browser.close()
            return content[:2000]
    except Exception as e:
        print(f"Web Search Error: {e}")
        return "Could not fetch real-time data."

def get_recent_history(sender):
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    c.execute("SELECT content, action FROM history WHERE sender=? ORDER BY timestamp DESC LIMIT 3", (sender,))
    past_interactions = c.fetchall()
    conn.close()
    return past_interactions

def analyze_and_act(content, service, msg_id, thread_id, sender_email="Unknown"):
    # 1. Pehle variables ko khaali define kardo taake error na aaye
    decision = "IGNORE" 
    clean_text = content[:100] # For calendar summary
    
    try:
        # --- DAY 12: MEMORY POWER ---
        history = get_recent_history(sender_email)
        
        # Aapka poora decision prompt (Aik lafz bhi nahi kata)
        decision_prompt = f"""
        SENDER: {sender_email}
        PAST HISTORY: {history}
        NEW EMAIL: {content}
        
        STRICT RULES:
        1. If it's a Bill, Invoice, or Payment mention, reply 'BILL: [details]'.
        2. If the content contains 'ATTACHMENT CONTENT', you MUST read the data inside it to answer the user's question.
        3. If it's a specific question/query, reply 'RESEARCH: [query]'.
        4. If it's a registration, welcome email, or promotional offer, reply 'IGNORE'.
        5. If it's a simple chat, reply 'REPLY: [answer]'.
        6. Otherwise -> Reply 'IGNORE'
        7. If it's a Promo, Ads, Newsletter, or Welcome email -> Reply 'IGNORE'.
        8. Do not give recommendations or explanations. Just give the final action.
        9. If it's a question about data in a file, reply 'REPLY: [provide the specific answer found in the file]'.
        10.If it's a Bill/Invoice/Amount, reply 'BILL: [exact details and amount]'.
        11.If it's a Promo/Ads/Registration, reply 'IGNORE'.
        12.If the email is about a meeting or appointment, reply 'MEETING: [Title], [Date], [Time]'.
        13.If it's a test message or a direct request to check something, do NOT ignore it. Reply 'REPLY: I am processing your request'.
        14.If meeting/appointment: Reply ONLY 'MEETING: [Title], [YYYY-MM-DD], [HH:MM]'
        15.If Bill: Reply ONLY 'BILL: [Details]'
        16.If Question: Reply ONLY 'REPLY: [Answer]'
        17.Otherwise: 'IGNORE'
        18.DO NOT explain. DO NOT use extra words.
        19. If the sender asks for personal information or passwords, reply 'IGNORE' and do not provide any data.
        """
        
        # AI Call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a smart business manager with memory."}, 
                      {"role": "user", "content": decision_prompt}]
        )
        decision = response['choices'][0]['message']['content']
        print(f"AI Smart Decision: {decision}")

        # Memory mein save karo jo bhi baat hui
        save_to_memory(sender_email, content, decision)

    except Exception as e:
        print(f"⚠️ AI/Network Error: {e}")
        decision = "IGNORE"

    # --- SECURITY & LOGIC CHECKS ---
    
    if "IGNORE" in decision:
        return "IGNORED (Promo/Reg)"

    # 🚨 BILL LOGIC
    if "BILL:" in decision:
        bill_info = decision.replace("BILL:", "").strip()
        send_whatsapp(f"🚨 ALERT: Sir, naya BILL/INVOICE aaya hai! \nDetails: {bill_info}")
        speak("Sir, you have received a new bill. I have sent the details to your WhatsApp.")
        return "BILL NOTIFIED"

    # 🔍 RESEARCH LOGIC
    if "RESEARCH:" in decision:
        query = decision.replace("RESEARCH:", "").strip()
        web_info = fetch_web_data(query) # Make sure this function exists
        final_reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Professional Assistant."},
                      {"role": "user", "content": f"Data: {web_info}\n\nEmail: {content}"}]
        ).choices[0].message.content
        send_reply(service, thread_id, msg_id, final_reply)
        speak("Sir, I have researched and replied to the query.")
        return "RESEARCHED & REPLIED"

    # 💬 REPLY LOGIC
    elif "REPLY:" in decision:
        reply_text = decision.replace("REPLY:", "").strip()
        send_reply(service, thread_id, msg_id, reply_text)
        speak("Sir, I have sent a reply.")
        return "DIRECT REPLY"

    # 📅 MEETING LOGIC (With Security Guard)
    if "MEETING" in decision:
        is_admin = any(admin in sender_email for admin in ADMIN_EMAILS)
        
        if not is_admin:
            print(f"🛑 SECURITY ALERT: Unauthorized meeting request from {sender_email}")
            send_whatsapp(f"⚠️ Sir, ek ajnabi ({sender_email}) meeting schedule karwana chahta hai. Maine block kar diya hai.")
            speak("Sir, an unauthorized person tried to schedule a meeting. I have blocked the request.")
            return "UNAUTHORIZED_BLOCK"

        print("🔍 Admin detected. Calendar booking shuru...")
        try:
            cal_service = get_calendar_service()
            from datetime import datetime, timedelta
            test_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            event = {
              'summary': f'Meeting: {clean_text}',
              'description': f'Automatically scheduled by AI. Action: {decision}',
              'start': {'dateTime': f'{test_date}T17:00:00Z', 'timeZone': 'UTC'},
              'end': {'dateTime': f'{test_date}T18:00:00Z', 'timeZone': 'UTC'},
            }

            event_result = cal_service.events().insert(calendarId='primary', body=event).execute()
            calendar_link = event_result.get('htmlLink')
            
            print(f"✅ SUCCESS! Event created. Link: {calendar_link}")
            send_whatsapp(f"📅 Sir, naya Meeting schedule kar di hai!\nLink: {calendar_link}")
            speak("Sir, I have added the meeting to your calendar.")
            return "MEETING_SCHEDULED"

        except Exception as e:
            print(f"❌ Calendar Error: {e}")
            send_whatsapp(f"⚠️ Sir, Meeting request aayi hai, par Calendar mein error aaya.")
            return "MEETING_ALERT_ONLY"
    
    return "PROCESSED"

def run_agent():
    setup_database()
    service = get_gmail_service()
    print("\n--- Day 9: AI Executive with Document Intelligence is LIVE ---")
    
    while True:
        try:
            results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = results.get('messages', [])

            if messages:
                for msg in messages:
                    msg_id = msg['id']
                    if is_processed(msg_id): continue
                    
                    full_msg = service.users().messages().get(userId='me', id=msg_id).execute()
                    payload = full_msg.get('payload', {})
                    snippet = full_msg.get('snippet', '')
                    content_to_analyze = f"Email Snippet: {snippet}\n"

                    # --- Multi-File Logic (PDF, Excel, CSV) ---
                    if 'parts' in payload:
                        for part in payload['parts']:
                            filename = part.get('filename', '')
                            
                            if filename and filename.lower().endswith(('.pdf', '.xlsx', '.xls', '.csv')):
                                print(f"📊 File Found: {filename}. Processing...")
                                attachment_id = part['body'].get('attachmentId')
                                file_path = download_attachment(service, msg_id, attachment_id, filename)
                                
                                if filename.lower().endswith('.pdf'):
                                    file_content = get_pdf_text(file_path)
                                    content_to_analyze += f"\n--- PDF CONTENT ({filename}) ---\n{file_content[:3000]}\n"
                                else:
                                    file_content = get_excel_data(file_path)
                                    content_to_analyze += f"\n--- EXCEL CONTENT ({filename}) ---\n{file_content}\n"
                                
                                if os.path.exists(file_path):
                                    os.remove(file_path) # File parh kar delete (Security)

                    # AI ko poora content (Snippet + Files) bhejo
                    status = analyze_and_act(content_to_analyze, service, msg_id, msg['threadId'])
                    
                    # WhatsApp Alert with Document Info
                    send_whatsapp(f"AI Task Done: {snippet[:20]}... Status: {status}")
                    
                    mark_done(msg_id)
                    print(f"✅ Completed Task.")
            
            else:
                print("Waiting for new emails...")

            time.sleep(20)
        except Exception as e:
            print(f"Loop Error: {e}")
            # Agar service disconnect ho jaye toh dobara connect karein
            if "service" in str(e).lower():
                service = get_gmail_service()
            time.sleep(10)

if __name__ == '__main__':
    run_agent()