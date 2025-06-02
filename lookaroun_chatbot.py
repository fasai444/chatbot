# LookAroun Simple Chatbot - Deployment Friendly
import streamlit as st
import re
import os

# Configure Streamlit page
st.set_page_config(
    page_title="LookAroun Assistant",
    page_icon="🤝",
    layout="wide"
)

# Comprehensive LookAroun knowledge base
LOOKAROUN_KNOWLEDGE = {
    # About LookAroun
    "what is lookaroun": "LookAroun is a mobile networking application designed specifically for B2B professional events. We help participants make targeted, meaningful connections through intelligent matching and real-time communication.",
    
    "how does lookaroun work": "LookAroun works by allowing participants to create detailed professional profiles, then uses smart filtering to help you find and connect with the most relevant people at your event. You can message directly through the app and build your professional network efficiently.",
    
    # Features
    "features": "LookAroun offers: 🎯 Smart participant matching, 💬 Instant messaging, 🔍 Advanced filtering by industry/role/goals, 📅 Event agenda integration, ⭐ Favorites system, 📱 Mobile-first design, and 🤝 Post-event contact management.",
    
    "smart matching": "Our intelligent targeting system analyzes your professional goals, industry, and networking objectives to suggest the most relevant connections at each event. No more random networking!",
    
    "messaging": "LookAroun includes built-in instant messaging so you can connect with other participants before, during, and after events. Start conversations easily and maintain professional relationships.",
    
    # Pricing
    "pricing": "We offer flexible pricing: 💫 Initiation plan (basic features, 3-day access), 🚀 Connexion plan (full features, 7-day access), ⭐ Influence plan (premium features, 14-day access), plus subscription options for frequent event organizers.",
    
    "cost": "LookAroun pricing varies by plan. Contact us for specific pricing details and to discuss which plan works best for your events and networking needs.",
    
    "free trial": "We offer demos and trial options! Contact us to schedule a free demonstration and see how LookAroun can transform networking at your events.",
    
    # For Event Organizers
    "event organizers": "For event organizers, LookAroun provides modern, engaging networking experiences that increase participant satisfaction. We handle setup, provide branded experiences, and offer analytics on networking success.",
    
    "organizer benefits": "Event organizers benefit from: ✨ Differentiated, modern event experience, 😊 Higher participant satisfaction, 📊 Networking analytics and insights, 🎨 Branded app customization, 💼 Sponsor value enhancement.",
    
    # For Participants
    "participant benefits": "Participants love LookAroun because it eliminates ineffective speed networking and random conversations. Instead, you get targeted connections with people who share your professional interests and goals.",
    
    "networking tips": "With LookAroun: 1) Complete your profile thoroughly, 2) Use filters to find relevant connections, 3) Read profiles before reaching out, 4) Start conversations with specific, relevant topics, 5) Follow up after events through the app.",
    
    # Technical
    "mobile app": "LookAroun is designed as a mobile-first application, optimized for use during live events. Easy to use while walking around, networking, and connecting with new professional contacts.",
    
    "setup": "Event setup is simple - we can handle the technical setup for you, or you can create events autonomously depending on your plan. Participants just download the app and join your event.",
    
    # Contact/Demo
    "demo": "Ready to see LookAroun in action? Contact us through our website to schedule a free demo. We'll show you exactly how LookAroun can improve networking at your events.",
    
    "contact": "You can reach us through our website contact form to schedule demos, ask questions, or discuss your specific event networking needs. We're here to help!",
    
    # Common questions
    "better than speed networking": "Unlike traditional speed networking which is often random and inefficient, LookAroun lets you pre-select who you want to meet based on professional relevance. Much more targeted and valuable!",
    
    "networking problems": "LookAroun solves common networking frustrations: random connections that don't lead anywhere, wasting time with irrelevant conversations, difficulty following up after events, and lack of structure in networking sessions."
}

# Conversation starters and responses
CONVERSATION_RESPONSES = {
    "hello": "Hello! I'm the LookAroun assistant. I can help you learn about our B2B networking app for professional events. What would you like to know?",
    
    "help": "I can help you with questions about LookAroun's features, pricing, how it works, benefits for event organizers and participants, or scheduling a demo. What interests you most?",
    
    "networking": "Great question about networking! LookAroun is designed to make professional networking much more effective and targeted. Instead of random conversations, you connect with people who match your specific professional goals and interests.",
    
    "events": "LookAroun specializes in B2B professional events - conferences, trade shows, corporate meetings, industry gatherings, and networking events. We make these events much more valuable for attendees."
}

def find_best_response(user_input):
    """Find the most relevant response based on user input"""
    user_lower = user_input.lower()
    
    # Remove common words and punctuation
    cleaned_input = re.sub(r'[^\w\s]', '', user_lower)
    words = cleaned_input.split()
    
    best_match = None
    best_score = 0
    
    # Check conversation starters first
    for key, response in CONVERSATION_RESPONSES.items():
        if key in user_lower:
            return response
    
    # Check knowledge base
    for key, response in LOOKAROUN_KNOWLEDGE.items():
        key_words = key.split()
        score = sum(1 for word in words if word in key_words)
        
        if score > best_score:
            best_score = score
            best_match = response
    
    # If no good match, provide helpful default
    if best_score == 0:
        if any(word in words for word in ['price', 'cost', 'money', 'pay']):
            return LOOKAROUN_KNOWLEDGE['pricing']
        elif any(word in words for word in ['how', 'work', 'use']):
            return LOOKAROUN_KNOWLEDGE['how does lookaroun work']
        elif any(word in words for word in ['demo', 'trial', 'test']):
            return LOOKAROUN_KNOWLEDGE['demo']
        else:
            return "I'd be happy to help you learn about LookAroun! You can ask me about our features, pricing, how it works, or request a demo. What interests you most?"
    
    return best_match

def main():
    st.title("🤝 LookAroun Assistant")
    st.markdown("*Your guide to smarter B2B networking*")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm here to help you learn about LookAroun, the smart networking app for B2B professional events. What would you like to know?"
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask me about LookAroun..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        response = find_best_response(prompt)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 LookAroun Features")
        st.markdown("• Smart participant matching")
        st.markdown("• Instant messaging")
        st.markdown("• Advanced filtering")
        st.markdown("• Event integration")
        st.markdown("• Post-event contacts")
        
        st.markdown("### 💬 Try asking:")
        st.markdown("• 'What is LookAroun?'")
        st.markdown("• 'How does pricing work?'")
        st.markdown("• 'What are the benefits?'")
        st.markdown("• 'Can I get a demo?'")
        st.markdown("• 'How is this better than speed networking?'")
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "Hello! I'm here to help you learn about LookAroun. What would you like to know?"
            }]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📞 Ready for a Demo?")
        st.markdown("Contact us to see LookAroun in action!")

if __name__ == "__main__":
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8501))
    
    # Run the app
    main()
