import streamlit as st
import sqlite3
import pandas as pd
import time
from text_to_sql_engine import generate_sql_from_gemini, extract_sql, generate_insight_from_data

# 1. PAGE SETUP
st.set_page_config(page_title="InsightX", layout="centered")

# 2. CUSTOM CSS INJECTION
st.markdown("""
<style>
    /* Import Poppins Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

    /* Apply Poppins Globally */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Centered Modern Heading */
    .modern-header {
        text-align: center;
        font-weight: 600;
        font-size: 2.8rem;
        letter-spacing: -1px;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }

    /* Style the Form container */
    [data-testid="stForm"] {
        border-radius: 20px !important;
        padding: 30px !important;
        transition: background-color 0.3s ease;
    }

    /* Gradient Submit Button */
    [data-testid="stFormSubmitButton"] > button {
        border-radius: 20px !important;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        transition: background 0.4s ease, transform 0.2s ease !important;
        width: 100%;
        margin-top: 10px;
    }
    
    [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
        transform: scale(1.02);
    }

    /* View Full Database Button Style */
    .stButton > button {
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }

    /* --- SYSTEM THEME ADAPTION --- */
    @media (prefers-color-scheme: dark) {
        [data-testid="stForm"] {
            background-color: #1e1e1e !important;
            border: 1px solid #333 !important;
        }
        div[data-baseweb="input"] > div {
            background-color: #ffffff !important;
            border-radius: 20px !important;
        }
        div[data-baseweb="input"] input { color: #000000 !important; }
        .stButton > button {
            background: transparent !important;
            border: 2px solid #3b82f6 !important;
            color: #3b82f6 !important;
        }
    }

    @media (prefers-color-scheme: light) {
        [data-testid="stForm"] {
            background-color: #f8f9fa !important;
            border: 1px solid #e5e7eb !important;
        }
        div[data-baseweb="input"] > div {
            background-color: #111827 !important;
            border-radius: 20px !important;
        }
        div[data-baseweb="input"] input { color: #ffffff !important; }
        .stButton > button {
            background: transparent !important;
            border: 2px solid #111827 !important;
            color: #111827 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown('<div class="modern-header">InsightX Analytics</div>', unsafe_allow_html=True)

# 4. USER INTERFACE
with st.form(key='query_form'):
    user_query = st.text_input("", placeholder="Ask a question about your transactions...")
    submit_button = st.form_submit_button(label="Generate Insights")

# 5. EXECUTION & RESULTS
if submit_button and user_query:
    with st.spinner("Analyzing database..."):
        try:
            # STEP 1: Generate SQL
            raw_sql = generate_sql_from_gemini(user_query)
            sql_query = extract_sql(raw_sql)
            
            # STEP 2: Execute SQL against REAL database
            db_name = 'transactions.db'
            conn = sqlite3.connect(db_name)
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            
            # STEP 3: Generate Factual Insight
            real_data_string = df.to_string() 
            insight = generate_insight_from_data(user_query, real_data_string)
            
            time.sleep(0.5) 
            st.markdown("---")
            
            # Display AI Insight
            st.markdown("### AI Insight")
            st.info(insight.replace("$", "₹"))
            
            # Display Results (Simplified Header)
            st.markdown("### Results") 
            
            if df.empty:
                st.warning("No records matched your criteria.")
            else:
                # Inject the actual SQL query as the table header
                if len(df.columns) == 1:
                    # If it's a single result (like an average), make the header the full SQL query
                    df.columns = [sql_query]

                # Format any currency values to Rupees
                for col in df.columns:
                    if any(x in col.lower() for x in ['amount', 'avg', 'sum', 'total', 'transaction']):
                        df[col] = df[col].apply(lambda x: f"₹{x:,.2f}" if isinstance(x, (int, float)) else x)
                
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            # AUTO-SCROLL
            st.components.v1.html(
                f"<script>window.parent.document.querySelector('.stSpinner').scrollIntoView({{behavior: 'smooth'}});</script>",
                height=0
            )

        except Exception as e:
            st.error(f"Error executing query: {e}")

# 6. FULL DATABASE LEDGER (Always at the bottom)
st.markdown("<br><br>", unsafe_allow_html=True)

if st.button("📂 View Full Database Ledger"):
    try:
        conn = sqlite3.connect('transactions.db')
        full_df = pd.read_sql_query("SELECT * FROM transactions LIMIT 100", conn)
        conn.close()
        
        st.write("### Raw Transaction Data (Top 100)")
        
        # Format the transaction_amount column to Rupees
        if 'transaction_amount' in full_df.columns:
            full_df['transaction_amount'] = full_df['transaction_amount'].map('₹{:,.2f}'.format)
            
        st.dataframe(full_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not load database: {e}")