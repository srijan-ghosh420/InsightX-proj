Here is a clean, professional **README.md** for your updated **InsightX Analytics Real-Time SQL Engine** project.

You can copy-paste this directly into your `README.md`.

---

# InsightX – AI Powered Real-Time Transaction Analytics Engine

InsightX is an AI-driven Text-to-SQL analytics engine that allows users to ask natural language questions about transaction data and receive:

* 🧠 Intelligent analytical insight
* 📜 Automatically generated SQL query
* 📊 Real-time database results

The system integrates **Google Gemini API** with a local **SQLite database** to create a smart analytics pipeline.

---

## 🚀 Features

* Natural Language → SQL conversion
* AI-generated analytical insight
* Real-time execution on SQLite
* Failure rate & percentage analysis
* Weekend vs weekday analytics
* Device-based analytics (Android / iOS / etc.)
* Modular architecture (Data Engine + SQL Engine + Main App)

---

## 🏗️ Project Structure

```
InsightX-proj/
│
├── data_engine.py              # Loads CSV → Cleans → Creates SQLite DB
├── text_to_sql_engine.py       # Gemini API → Insight + SQL extraction
├── main_app.py                 # Main interactive analytics engine
│
├── transactions.db             # SQLite database (auto-generated)
├── insightx_transactions.csv   # Dataset
│
├── .env                        # Stores Gemini API Key (NOT pushed to GitHub)
├── .gitignore
└── README.md
```

---

## ⚙️ System Architecture

```
User Question
      ↓
Gemini API (Text → Insight + SQL)
      ↓
SQL Extraction Engine
      ↓
SQLite Database Execution
      ↓
Results + Insight Displayed
```

---

## 🧠 Example Query

```
What is the failure percentage of Android transactions?
```

### Output:

**AI Insight**

> The failure rate for Android transactions is calculated to evaluate platform reliability.

**Generated SQL**

```sql
SELECT (SUM(CASE WHEN transaction_status = 'FAILED' THEN 1 ELSE 0 END) * 100.0) / COUNT(*)
FROM transactions
WHERE device_type = 'Android';
```

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/srijan-ghosh420/InsightX-proj.git
cd InsightX-proj
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If no requirements file exists, install manually:

```bash
pip install pandas sqlite3 python-dotenv google-generativeai
```

---

### 4️⃣ Setup Environment Variable

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

### 5️⃣ Create Database

Run:

```bash
python data_engine.py
```

This will:

* Load CSV
* Clean column names
* Create `transactions` table
* Generate `transactions.db`

---

### 6️⃣ Run the Main Application

```bash
python main_app.py
```

You will see:

```
--- InsightX Analytics Real-Time SQL Engine ---
Ask a question about your transactions:
```

---

## 🧩 Key Modules

### 🔹 data_engine.py

* Loads dataset
* Cleans column names
* Renames important columns
* Creates SQLite database table: `transactions`

---

### 🔹 text_to_sql_engine.py

* Sends prompt to Gemini
* Extracts:

  * AI Insight
  * SQL Query
* Returns both separately

---

### 🔹 main_app.py

* Accepts user query
* Calls AI engine
* Executes SQL
* Displays:

  * Insight
  * Generated SQL
  * Query Result

---

## 📌 Important Notes

* The table name must be `transactions`
* Do NOT push:

  * `.env`
  * `.db`
  * `.csv`
* Ensure `.gitignore` contains:

```
.env
*.db
*.csv
__pycache__/
```

---

## 🧪 Example Analytics Supported

* Failure rate by device type
* Weekend vs weekday performance
* Transaction count by category
* Success vs failed ratio
* Average transaction amount
* Platform reliability comparison

---

## 🔐 Security

* API keys stored in `.env`
* No secrets pushed to GitHub
* SQLite local database only

---

## 📈 Future Improvements

* Streamlit Web Dashboard
* Chart Visualization
* Multi-table Support
* Caching Layer
* Error Correction for AI-generated SQL
* Cloud Deployment

---

## 👨‍💻 Author

**Srijan Ghosh**
AI/ML + Data Engineering Enthusiast
Project: InsightX – Intelligent Analytics Engine
