import streamlit as st
import base64

def show():
    # Title and description
    st.title("Welcome to Mino")
    st.write("Your personal AI assistant is here to help!")
    
    # Read and encode video file
    with open("my.mp4", "rb") as video_file:
        video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
    
    # Center the video using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Custom video player with autoplay and no controls
        st.markdown(f"""
        <style>
        #myvideo {{
            width: 100%;
            border-radius: 10px;
            margin: 20px auto;
        }}
        video::-webkit-media-controls {{
            display: none !important;
        }}
        video::-webkit-media-controls-enclosure {{
            display: none !important;
        }}
        </style>
        <video id="myvideo" autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True)
    
    # Login button centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login / Sign Up", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun() 