import streamlit as st
from db import execute_query, get_tables

# Add this at the very start to help debug
st.set_page_config(page_title="Gripdata SQL Practice", layout="wide")

st.title("Gripdata SQL Practice")
try:
    # Get list of tables
    
    tables = get_tables()
   
    
    # Create main layout
    left_col, right_col = st.columns([3, 1])
    
    with right_col:
        st.header("Tables")
        selected_table = st.selectbox(
            "Select a table:",
            tables
        )
        
        if selected_table:
            if st.button("Show Sample Data"):
                sample_query = f"SELECT * FROM {selected_table} LIMIT 5"
                sample_df = execute_query(sample_query)
                st.dataframe(sample_df)
    
    with left_col:
        st.info("""
        ℹ️ **Instructions:**
        1. Select a table from the right panel
        2. Write your PostgreSQL query below
        3. Click 'Execute' to see results
        """)
        
        # Query input
        query = st.text_area("Enter your PostgreSQL query:", height=200)
        
        # Execute button
        if st.button("Execute Query", type="primary"):
            try:
                if query.strip():
                    df = execute_query(query)
                    st.success("Query executed successfully!")
                    st.dataframe(df)
                    
                    # Add download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("Please enter a query first.")
                    
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
    
    # Add footer with attribution
    st.markdown("""
    ---
    Made with ❤️ by Amlan for GripData Analytics
    
    [GitHub](https://github.com/amlanacharya) | [LinkedIn](https://www.linkedin.com/in/amlan-acharya/)
    """)

except Exception as e:
    st.error(f"Error in main app: {str(e)}")
    st.error("Full error details:")
    st.exception(e) 