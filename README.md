Here’s a clean, professional **README.md** for your `InsightX-proj` repository.
You can copy-paste this directly into your `README.md`.

---

# 📊 InsightX – Text-to-SQL Transaction Analytics Engine

InsightX is a lightweight Text-to-SQL analytics system that converts natural language queries into SQL queries and executes them on a transaction database.

It enables users to ask questions like:

* *"What is the lowest transaction amount?"*
* *"Show total successful transactions."*
* *"Average transaction amount by category."*

and automatically generates and executes SQL on a SQLite database.

---

## 🚀 Features

* 🔎 Natural Language → SQL conversion
* 🗄 SQLite database integration
* 📂 CSV transaction dataset loader
* 🧠 LLM-powered query generation
* 📊 Automated query execution
* 🛠 Modular architecture

---

## 📁 Project Structure

```
insightx/
│
├── data_engine.py              # Handles dataset loading & DB creation
├── text_to_sql_engine.py       # Converts natural language to SQL
├── main_app.py                 # Entry point of application
├── insightx_database.db        # SQLite database (ignored in git)
├── transactions.db             # SQLite database (ignored in git)
├── insightx_transactions.csv   # Dataset (ignored in git)
├── .env                        # API keys (ignored in git)
└── __pycache__/                # Python cache (ignored in git)
```

---

## 🧩 Tech Stack

* Python 3.9+
* SQLite
* Pandas
* Python-dotenv
* Google Generative AI (Gemini API)

---

## 📦 Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, install manually:

```bash
pip install pandas python-dotenv google-generativeai sqlite3
```

> ⚠️ `sqlite3` comes pre-installed with Python. No separate installation needed.

---

## 🔑 Environment Setup

Create a `.env` file in the root folder:

```
GEMINI_API_KEY=your_api_key_here
```

Do NOT commit this file.

---

## 🛠 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/InsightX-proj.git
cd InsightX-proj
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
python main_app.py
```

---

## 🗄 Database Workflow

1. `data_engine.py`

   * Loads CSV
   * Cleans column names
   * Creates SQLite database

2. `text_to_sql_engine.py`

   * Takes user query
   * Sends to Gemini
   * Generates SQL

3. `main_app.py`

   * Executes SQL
   * Returns results

---

## 🧠 Example Query

```
Enter your query:
> what is the lowest transaction amount
```

Generated SQL:

```
SELECT MIN(transaction_amount) FROM transactions;
```

Output:

```
Lowest Transaction Amount: 120
```

---

## 🔒 Ignored Files

The following are excluded using `.gitignore`:

```
.env
*.db
insightx_transactions.csv
__pycache__/
*.pyc
```

---

## 🔮 Future Improvements

* Web interface (Streamlit / Flask)
* Query history tracking
* Dashboard visualization
* Multi-database support
* Better prompt engineering

---

## 👨‍💻 Author

Srijan Ghosh
InsightX Project

---
