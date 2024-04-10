import streamlit as st
import pyodbc
import pandas as pd
import hashlib
import secrets
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    driver = st.secrets["driver"]
    server = st.secrets["server"]
    database = st.secrets["database"]
    username = st.secrets["username"]
    password = st.secrets["password"]
    conn_str = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)

def add_job(job_name, job_description, main_table, category, progress, begin_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Jobs (JobName, JobDescription, mainTable, Category, Progress, BeginDate, EndDate) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, job_name, job_description, main_table, category, progress, begin_date, end_date)
    conn.commit()
    conn.close()

st.title('Lisää tiedot')

st.sidebar.subheader('Add New User')
username = st.sidebar.text_input('Username', key='new_user_username')
if st.sidebar.button('Generate and Add User'):
    new_password = secrets.token_urlsafe(8)  # Generate a random password
    add_user(username, new_password)
    st.sidebar.write(f"User added with password: {new_password}")

st.sidebar.subheader('Add New Job')
job_name = st.sidebar.text_input('Job Name', key='new_job_name')
job_description = st.sidebar.text_area('Job Description', key='new_job_description')
main_table = st.sidebar.text_input('Main Table', key='new_job_main_table')
category = st.sidebar.text_input('Category', key='new_job_category')
progress = st.sidebar.text_input('Progress', key='new_job_progress') 
begin_date = st.sidebar.date_input('Begin Date', key='new_job_begin_date')
end_date = st.sidebar.date_input('End Date', key='new_job_end_date')

if st.sidebar.button('Add Job'):
    add_job(job_name, job_description, main_table, category, progress, begin_date, end_date)
    st.sidebar.success('Job added successfully.')

st.markdown('## Update Existing Records')

