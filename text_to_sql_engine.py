import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Force Python to look for .env in this exact same folder
current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path=env_file_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(f"❌ ERROR: Could not find GEMINI_API_KEY in: {env_file_path}")
    print("Please make sure your .env file is saved and contains your key!")
    exit()

# 2. Configure the modern Gemini API Client
client = genai.Client(api_key=api_key)

# 3. Define the massive System Prompt
SYSTEM_PROMPT = """
You are an expert Data Analyst and SQL Developer for a digital payments company.
Your goal is to translate user questions into strictly valid SQLite queries.

DATABASE SCHEMA:
Table Name: transactions
Columns:
- transaction_id (TEXT): Unique ID
- transaction_amount (FLOAT): Amount in INR
- transaction_type (TEXT): 'P2P' (Person-to-Person) or 'P2M' (Person-to-Merchant)
- sender_bank (TEXT): Bank initiating the transfer
- transaction_status (TEXT): 'SUCCESS', 'FAILED', or 'PENDING'
- merchant_category (TEXT): Merchant type. Note: NULL or 'N/A' for P2P transactions.
- fraud_flag (INTEGER): 1 if flagged for review, 0 otherwise.
- is_weekend (INTEGER): 1 if weekend, 0 if weekday.
- hour_of_day (INTEGER): 0-23 representing the hour.
- network_type (TEXT): '4G', '5G', 'WiFi'
- device_type (TEXT): 'Android', 'iOS'
- sender_age_group (TEXT)
- receiver_age_group (TEXT)
- time_block (TEXT): 'Morning', 'Afternoon', 'Peak Evening', 'Late Night'
- is_high_value (INTEGER): 1 if amount >= 5000

BUSINESS RULES:
1. "Failure Rate": Calculated as (SUM(CASE WHEN transaction_status = 'FAILED' THEN 1 ELSE 0 END) * 100.0) / COUNT(*).
2. "High Value": Refers to transaction_amount > 5000.
3. Handle Case-Insensitivity: Always use UPPER() or strictly match exactly as data is formatted.

OUTPUT INSTRUCTIONS:
Return ONLY the raw SQL query. Do not include any explanations, apologies, or conversational text.
"""

# 4. Create the function to call Gemini (using the new SDK format)
def generate_sql_from_gemini(user_query):
    print(f"🧠 Sending query to Gemini: '{user_query}'...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0,
        )
    )
    
    return response.text

# 5. Create a function to clean the markdown out of the response
def extract_sql(llm_response):
    match = re.search(r'```sql\n(.*?)\n```', llm_response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_response.replace('```', '').strip()

# --- TEST THE CONNECTION ---
if __name__ == "__main__":
    print("✅ System initialized. Testing API connection...\n")
    test_question = "What is the failure rate for Android users on Weekends?"
    
    try:
        raw_output = generate_sql_from_gemini(test_question)
        clean_sql = extract_sql(raw_output)
        
        print("\n✨ Gemini generated this SQL:")
        print("-" * 40)
        print(clean_sql)
        print("-" * 40)
        print("\n🎉 If you see a SQL query above, your AI Engine is successfully connected!")
        
    except Exception as e:
        print(f"\n❌ ERROR connecting to Gemini: {e}")
