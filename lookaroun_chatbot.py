# LookAroun Free Chatbot

import streamlit as st
from transformers import pipeline, Conversation
import time

# Configure Streamlit page
st.set_page_config(
    page_title="LookAroun Assistant",
    page_icon="🤝",
    layout="wide"
)

#to avoid reloading
@st.cache_resource
def load_chatbot():
    """Load the conversational AI model  this will download 500MB first time"""
    try:
        return pipeline("conversational", model="microsoft/DialoGPT-small")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

#  knowledge base
LOOKAROUN_INFO = {
    "what is lookaroun": "LookAroun is a mobile networking app for B2B professional events. It helps participants make targeted connections through smart matching and real-time messaging.",
    "pricing": "We offer several plans: Initiation (basic features), Connexion (7-day access), Influence (14-day access), and subscription plans for event organizers.",
    "how it works": "LookAroun uses intelligent targeting to match participants based on their professional goals. You can filter, message, and connect with the right people at events.",
    "features": "Key features include: smart participant matching, instant messaging, advanced filters, event agenda integration, and post-event contact management.",
    "demo": "Contact us through our website to schedule a free demo. We'll show you how LookAroun can improve networking at your events."
}

def get_lookaroun_response(user_input):
    """Check if user question matches LookAroun knowledge base"""
    user_lower = user_input.lower()
    
    for key, response in LOOKAROUN_INFO.items():
        if any(word in user_lower for word in key.split()):
            return response
    
    return None

def main():
    st.title(" LookAroun Assistant")
    st.markdown("*Your AI helper for professional networking questions*")
    
    # Load the chatbot
    with st.spinner("Loading AI model (this may take a moment the first time)..."):
        chatbot = load_chatbot()
    
    if chatbot is None:
        st.error("Failed to load the AI model. Please refresh the page.")
        return
    
    # Initialize conversation in session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # User input
    user_input = st.chat_input("Ask me about LookAroun or networking...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # First check LookAroun knowledge base
                lookaroun_response = get_lookaroun_response(user_input)
                
                if lookaroun_response:
                    response = lookaroun_response
                else:
                    # Use AI model for general conversation
                    try:
                        if st.session_state.conversation is None:
                            st.session_state.conversation = Conversation(user_input)
                        else:
                            st.session_state.conversation.add_user_input(user_input)
                        
                        st.session_state.conversation = chatbot(st.session_state.conversation)
                        response = st.session_state.conversation.generated_responses[-1]
                        
                        # Add context about LookAroun if response seems generic
                        if len(response) < 20 or "networking" in user_input.lower():
                            response += " For professional networking events, LookAroun can help you make more meaningful connections efficiently."
                            
                    except Exception as e:
                        response = "I'm having some technical difficulties. Could you try rephrasing your question about LookAroun or networking?"
                
                st.write(response)
                
                # Add assistant response to history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### About LookAroun")
        st.markdown(" **Smart networking for B2B events**")
        st.markdown(" **Instant messaging**")
        st.markdown(" **Advanced participant filtering**")
        st.markdown(" **Event agenda integration**")
        
        st.markdown("---")
        st.markdown("### Quick Commands")
        st.markdown("Try asking:")
        st.markdown("- 'What is LookAroun?'")
        st.markdown("- 'How does pricing work?'")
        st.markdown("- 'What features do you have?'")
        st.markdown("- 'How can I get a demo?'")
        
        st.markdown("---")
        if st.button("Clear Chat History"):
            st.session_state.conversation = None
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()