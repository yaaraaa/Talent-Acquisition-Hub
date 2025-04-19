import streamlit as st
from chatbot.api import ChatbotAPIClient
import os

def chatbot_page():
    st.header("💬 Chat with Your Assistant")

    api_client = ChatbotAPIClient(api_base_url = f"{os.getenv('BACKEND_URL')}/chatbot") # Base URL for the chatbot API

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Custom CSS for styling messages
    st.markdown(
        """
        <style>
        .chat-message {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }
        .chat-message .icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            margin-right: 10px;
        }
        .chat-message.user .icon {
            background-color: #007bff; /* Blue for user icon */
        }
        .chat-message.bot .icon {
            background-color: #d6d8db; /* Lighter gray for bot icon */
        }
        .chat-message .message {
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 10px 15px;
            max-width: 90%; /* Increase width to 90% */
            word-wrap: break-word;
        }
        .chat-message.user .message {
            background-color: #cce5ff; /* Light blue for user message */
        }
        .chat-message.bot .message {
            background-color: #f1f1f1; /* Default gray for bot message */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display chat history dynamically
    chat_placeholder = st.container()
    with chat_placeholder:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat-message user">
                        <div class="icon">🧑</div>
                        <div class="message">{chat['message']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-message bot">
                        <div class="icon">🤖</div>
                        <div class="message">{chat['message']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Input form for new messages
    user_input = st.text_input("Your message:")
    if st.button("Send"):
        if user_input.strip():
            # Add user's message to chat history
            st.session_state.chat_history.append({"role": "user", "message": user_input})

            # Send message to the chatbot API
            with st.spinner("Assistant is typing..."):
                collection_name = st.session_state.collection_name
                response = api_client.send_message(collection_name, user_input)
                print(response)

                if response["success"]:
                    bot_response = response["response"]["response"]
                    st.session_state.chat_history.append({"role": "bot", "message": bot_response})
                else:
                    st.error("Error communicating with the chatbot.")
                    if "details" in response:
                        st.text(response["details"])

            # Clear the input box
            st.rerun()

    # Clear chat history
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
