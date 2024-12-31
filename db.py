import streamlit as st
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:8bxtCjgoMp3e@ep-crimson-mud-a1z41eov.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

@st.cache_resource
def get_database_connection():
    """Create and cache database connection"""
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

def get_tables():
    """Get list of tables"""
    engine = get_database_connection()
    if engine is None:
        return []
    
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name
    """
    return pd.read_sql_query(query, engine)['table_name'].tolist()

def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    try:
        engine = get_database_connection()
        if engine is None:
            return None
        
        return pd.read_sql_query(query, engine)
    except Exception as e:
        raise Exception(f"Error executing query: {str(e)}")
