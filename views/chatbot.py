import streamlit as st
from transformers import pipeline
from datetime import datetime
import os
import base64

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def get_image_base64():
    with open("ai.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def show():
    # Check if user is logged in
    if not st.session_state.get("logged_in", False):
        st.session_state.page = "login"
        st.rerun()

    # Initialize session state for messages if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_session_date" not in st.session_state:
        st.session_state.current_session_date = datetime.now().strftime("%B %d, %Y")

    # Load model
    @st.cache_resource
    def load_model():
        return pipeline("text2text-generation", model="facebook/blenderbot-400M-distill", 
                      framework="pt")

    # Get AI image as base64
    ai_image = get_image_base64()
    # Get user profile image
    user_image = st.session_state.get("user_profile_image", None)

    # Custom CSS for AI image and chat
    st.markdown(f"""
    <style>
    .ai-title {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .ai-title img {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }}
    .ai-chat-image, .user-chat-image {{
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 10px;
        object-fit: cover;
    }}
    .chat-message {{
        display: flex;
        align-items: start;
        gap: 10px;
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
    }}
    .user-message {{
        background: rgba(255, 255, 255, 0.05);
        margin-left: 40px;
    }}
    .assistant-message {{
        background: rgba(255, 255, 255, 0.02);
    }}
    .message-time {{
        font-size: 0.8em;
        opacity: 0.8;
        margin-bottom: 5px;
    }}
    /* Hide default Streamlit message styling */
    .stChatMessage {{
        background: transparent !important;
        border: none !important;
    }}
    .stChatMessage [data-testid="stChatMessageContent"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    /* Custom chat input styling */
    .chat-input-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 10px;
        margin-top: 20px;
    }}
    .chat-input-container img {{
        width: 30px;
        height: 30px;
        border-radius: 50%;
        object-fit: cover;
    }}
    .stTextInput {{
        flex-grow: 1;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Main chat interface
    col1, col2 = st.columns([1, 3])

    with col1:
        st.sidebar.title("Chat History")
        st.sidebar.markdown(f"### {st.session_state.current_session_date}")
        # Display message previews in sidebar
        for message in st.session_state.messages:
            preview = message['content'][:30] + "..." if len(message['content']) > 30 else message['content']
            st.sidebar.markdown(f"- {preview}")
        
        # Add logout button at the bottom of sidebar using empty space
        st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True)
        if st.sidebar.button("Logout", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.messages = []
            st.session_state.page = "home"
            st.rerun()

    with col2:
        # Header with title and clear chat button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.markdown(f"""
            <div class="ai-title">
                <img src="data:image/jpeg;base64,{ai_image}" alt="AI Assistant">
                <h1>Mino</h1>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"Welcome back, {st.session_state.username}!")
        with header_col2:
            if st.button("Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.rerun()

        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "assistant":
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <img src="data:image/jpeg;base64,{ai_image}" class="ai-chat-image" alt="AI">
                        <div>
                            <div class="message-time">{message.get('time', '')}</div>
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        {f'<img src="data:image/jpeg;base64,{user_image}" class="user-chat-image" alt="User">' if user_image else ''}
                        <div>
                            <div class="message-time">{message.get('time', '')}</div>
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Custom chat input with user image
        st.markdown(f"""
        <div class="chat-input-container">
            {f'<img src="data:image/jpeg;base64,{user_image}" alt="User">' if user_image else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("What is on your mind?"):
            current_time = datetime.now().strftime("%I:%M %p")
            
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "time": current_time
            })

            # Display user message
            st.markdown(f"""
            <div class="chat-message user-message">
                {f'<img src="data:image/jpeg;base64,{user_image}" class="user-chat-image" alt="User">' if user_image else ''}
                <div>
                    <div class="message-time">{current_time}</div>
                    {prompt}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Generate response
            with st.spinner("Thinking..."):
                try:
                    chatbot = load_model()
                    response = chatbot(prompt, max_length=100)[0]['generated_text']
                except Exception as e:
                    response = "I apologize, but I'm having trouble generating a response right now. Please try again."
                
                current_time = datetime.now().strftime("%I:%M %p")
                
                # Display assistant message
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <img src="data:image/jpeg;base64,{ai_image}" class="ai-chat-image" alt="AI">
                    <div>
                        <div class="message-time">{current_time}</div>
                        {response}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "time": current_time
                }) 