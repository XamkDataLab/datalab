import streamlit as st
import pyodbc
import pandas as pd
import hashlib
import random
import string
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

def add_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    # Adjust the INSERT statement according to your 'Users' table schema
    query = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
    cursor.execute(query, username, hashed_password)
    conn.commit()
    conn.close()

def add_job(job_name, job_description, main_table, category, progress, begin_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Jobs (JobName, JobDescription, mainTable, Category, Progress, begin_date, end_date) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, job_name, job_description, main_table, category, progress, begin_date, end_date)
    conn.commit()
    conn.close()

def generate_password():
    return ''.join(random.choices(string.ascii_letters, k=6))

def update_job(job_id, job_name, job_description, main_table, category, progress, begin_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    UPDATE Jobs 
    SET JobName = ?, JobDescription = ?, mainTable = ?, Category = ?, Progress = ?, begin_date = ?, end_date = ? 
    WHERE JobID = ?
    """
    cursor.execute(query, job_name, job_description, main_table, category, progress, begin_date, end_date, job_id)
    conn.commit()
    conn.close()

st.title('Lisää tiedot')

st.subheader('Add New User')
username = st.text_input('Username', key='new_user_username')
if st.button('Generate and Add User'):
    new_password = generate_password() 
    add_user(username, new_password)
    st.write(f"New user {username} created with password: {new_password}")

st.subheader('Add New Job')
job_name = st.text_input('Job Name', key='new_job_name')
job_description = st.text_area('Job Description', key='new_job_description')
main_table = st.text_input('Main Table', key='new_job_main_table')
category = st.text_input('Category', key='new_job_category')
progress = st.text_input('Progress', key='new_job_progress') 
begin_date = st.date_input('Begin Date', key='new_job_begin_date')
end_date = st.date_input('End Date', key='new_job_end_date')

if st.button('Add Job'):
    add_job(job_name, job_description, main_table, category, progress, begin_date, end_date)
    st.success('Job added successfully.')

st.subheader('Update existing job')

job_id_to_update = st.number_input('Enter Job ID to Update', value=0, step=1)

update_job_name = st.text_input('Job Name', key='update_job_name')
update_job_description = st.text_area('Job Description', key='update_job_description')
update_main_table = st.text_input('Main Table', key='update_job_main_table')
update_category = st.text_input('Category', key='update_job_category')
update_progress = st.text_input('Progress', key='update_job_progress')
update_begin_date = st.date_input('Begin Date', key='update_job_begin_date')
update_end_date = st.date_input('End Date', key='update_job_end_date')

if st.button('Update Job'):
    update_job(job_id_to_update, update_job_name, update_job_description, update_main_table, update_category, update_progress, update_begin_date, update_end_date)
    st.success(f'Job ID {job_id_to_update} updated successfully.')

