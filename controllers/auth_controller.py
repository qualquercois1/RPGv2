import streamlit as st
import bcrypt
from models.user import User
from database import create_tables

def init_database():
    create_tables()

def register(username, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    return new_user.save()
    
def login(username, password):
    user = User.get_user_by_name(username)

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            st.session_state['logged_in'] = True
            st.session_state['username'] = user.username
            st.session_state['user_id'] = user.id

            return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_id'] = None
