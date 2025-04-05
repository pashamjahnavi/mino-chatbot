import streamlit as st
import mysql.connector
from db_config import get_db_connection
import hashlib
import base64
from PIL import Image
import io

def get_image_base64():
    with open("ai.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def convert_image_to_base64(image):
    # Convert PIL Image to base64 string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def show():
    # Get AI image
    ai_image = get_image_base64()
    
    # Custom CSS for login page
    st.markdown(f"""
    <style>
    .login-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 2rem;
        text-align: center;
    }}
    .login-header img {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .profile-upload {{
        margin: 20px 0;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
    }}
    .profile-preview {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin: 10px auto;
        display: block;
        object-fit: cover;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .upload-label {{
        color: #ffffff;
        opacity: 0.8;
        font-size: 0.9em;
        margin-bottom: 10px;
        display: block;
    }}
    /* Hide file uploader label */
    .uploadedFile {{
        display: none;
    }}
    </style>
    
    <div class="login-header">
        <img src="data:image/jpeg;base64,{ai_image}" alt="AI Assistant">
        <h1>Welcome to Mino</h1>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()

    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login tab
    with tab1:
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            
            # Profile picture upload
            st.markdown('<div class="profile-upload">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Profile Picture (optional)", type=['jpg', 'jpeg', 'png'], key="login_uploader")
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                # Resize image to a reasonable size
                image.thumbnail((200, 200))
                st.image(image, use_column_width=False, width=100, clamp=True)
                # Store image in session state temporarily
                st.session_state.temp_profile_image = convert_image_to_base64(image)
            st.markdown('</div>', unsafe_allow_html=True)
            
            login_submit = st.form_submit_button("Login")
            
            if login_submit:
                if not login_username or not login_password:
                    st.error("Please enter both username and password!")
                else:
                    conn = get_db_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            # Hash the password
                            hashed_password = hashlib.sha256(login_password.encode()).hexdigest()
                            
                            # Check credentials
                            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                                         (login_username, hashed_password))
                            user = cursor.fetchone()
                            
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.username = login_username
                                # Store profile image in session state if uploaded
                                if 'temp_profile_image' in st.session_state:
                                    st.session_state.user_profile_image = st.session_state.temp_profile_image
                                st.success("Login successful!")
                                st.session_state.page = "chatbot"
                                st.experimental_rerun()
                            else:
                                st.error("Invalid username or password")
                        except mysql.connector.Error as err:
                            st.error(f"Database error: {err}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        st.error("Could not connect to database. Please try again later.")

    # Signup tab
    with tab2:
        with st.form("signup_form"):
            signup_username = st.text_input("Choose Username")
            signup_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            # Profile picture upload
            st.markdown('<div class="profile-upload">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Profile Picture (optional)", type=['jpg', 'jpeg', 'png'], key="signup_uploader")
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                # Resize image to a reasonable size
                image.thumbnail((200, 200))
                st.image(image, use_column_width=False, width=100, clamp=True)
                # Store image in session state temporarily
                st.session_state.temp_profile_image = convert_image_to_base64(image)
            st.markdown('</div>', unsafe_allow_html=True)
            
            signup_submit = st.form_submit_button("Sign Up")
            
            if signup_submit:
                if not signup_username or not signup_password or not confirm_password:
                    st.error("Please fill in all fields!")
                elif signup_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    conn = get_db_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            
                            # Check if username exists
                            cursor.execute("SELECT * FROM users WHERE username = %s", (signup_username,))
                            if cursor.fetchone():
                                st.error("Username already exists!")
                            else:
                                # Hash the password
                                hashed_password = hashlib.sha256(signup_password.encode()).hexdigest()
                                
                                # Insert new user
                                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                                             (signup_username, hashed_password))
                                conn.commit()
                                
                                # Store profile image in session state if uploaded
                                if 'temp_profile_image' in st.session_state:
                                    st.session_state.user_profile_image = st.session_state.temp_profile_image
                                
                                st.success("Account created successfully! Please login.")
                                st.experimental_rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Database error: {err}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        st.error("Could not connect to database. Please try again later.") 