# 📊 InsightX Analytics

InsightX Analytics is an AI-powered Text-to-SQL engine built with Python and Streamlit. It allows users to ask natural language questions about their transaction data, automatically generates and executes the correct SQL query, and provides a structured, factual AI insight based *strictly* on the returned data.

## ✨ Features

* **Natural Language Querying:** Ask questions in plain English (e.g., "What was the average transaction amount in March?").
* **Transparent SQL Generation:** Displays the exact SQL query executed against the database directly in the results table.
* **Factual AI Insights:** Generates a structured 4-point business report (Direct Response, Statistics, Context, Recommendations) based strictly on real database results to prevent hallucination.
* **Smart Formatting:** Automatically formats monetary values to Indian Rupees (₹) across the UI and AI insights.
* **Modern UI:** Responsive, dark/light mode compatible interface with clean typography and gradient elements.

---

## 🛠️ Prerequisites

Make sure you have the following installed on your system:

* [Python 3.8+](https://www.python.org/downloads/)
* Pip (Python package manager)
* A valid Google Gemini API Key (for the `text_to_sql_engine.py`)

---

## 📦 Installation & Setup

**1. Clone or download the repository**
Navigate to the project folder in your terminal.

**2. Create a Virtual Environment (Recommended)**
python -m venv venv

**3. Activate the Virtual Environment**

* **Windows:**
venv\Scripts\activate
* **Mac/Linux:**
source venv/bin/activate

**4. Install Dependencies**
Create a `requirements.txt` file in your directory with the following packages, then run the install command.

*requirements.txt contents:*
streamlit
pandas
google-generativeai

*Run:*
pip install -r requirements.txt

**5. Database & API Key Configuration**

* Ensure your `transactions.db` SQLite database is in the root directory.
* Ensure your Gemini API key is properly configured in your `text_to_sql_engine.py` file or environment variables.

---

## 🚀 Running the Application

To run the application manually from your terminal, execute:
streamlit run app.py

The app will automatically open in your default web browser at `http://localhost:8501`.

---

## ⚡ Quick Start Scripts (Terminal Executables)

If you want to run the app with a single click or a single terminal command without manually typing the activation and run commands every time, create one of the following files in your project directory:

### For Windows (`start.bat`)

Create a new text file, paste this code, and save it as `start.bat`. You can now double-click this file to launch the app.

@echo off
echo =========================================
echo   Starting InsightX Analytics...
echo =========================================

REM Check if virtual environment exists, create if not
if not exist venv\Scripts\activate (
echo Creating virtual environment...
python -m venv venv
)

REM Activate and run
call venv\Scripts\activate
echo Installing/Checking dependencies...
pip install -r requirements.txt -q
echo Launching Streamlit...
streamlit run app.py
pause

### For Mac/Linux (`start.sh`)

Create a new file, paste this code, and save it as `start.sh`. Remember to make the script executable by running `chmod +x start.sh` in your terminal first.

#!/bin/bash
echo "========================================="
echo "  Starting InsightX Analytics..."
echo "========================================="

# Check if virtual environment exists, create if not

if [ ! -d "venv" ]; then
echo "Creating virtual environment..."
python3 -m venv venv
fi

# Activate and run

source venv/bin/activate
echo "Installing/Checking dependencies..."
pip install -r requirements.txt -q
echo "Launching Streamlit..."
streamlit run app.py
