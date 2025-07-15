import streamlit as st
import os
import time

from scraper.reddit_scraper import scrape_user, save_user_data
from processor.text_cleaner import clean_user_data, save_cleaned_data
from llm_engine.persona_builder import generate_persona
from avatar.avatar_generator import generate_avatar_url

# Set page configuration
st.set_page_config(
    page_title="Reddit Persona Generator",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': 'Reddit User Persona Generator'
    }
)

# Custom CSS for dark theme
st.markdown("""
<style>
.stApp {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
.persona-card {
    background-color: #2D2D2D;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    color: #FFFFFF;
}
.quote-text {
    font-style: italic;
    color: #B0B0B0;
    border-left: 3px solid #ff4500;
    padding-left: 1rem;
}
.stButton>button {
    background-color: #ff4500;
    color: white;
}
.stTextInput>div>div>input {
    background-color: #3D3D3D;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='color: #FFFFFF;'>🎯 Reddit User Persona Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #B0B0B0;'>Generate detailed user personas from Reddit activity</p>", unsafe_allow_html=True)

# Input form
with st.form("input_form", clear_on_submit=True):
    username_input = st.text_input("Enter Reddit Username", placeholder="username (without u/)", help="Enter the Reddit username without 'u/' prefix")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submitted = st.form_submit_button("🔍 Generate Persona", use_container_width=True)

if submitted and username_input:
    # Progress tracking
    progress = st.progress(0)
    
    # Step 1: Scraping
    with st.spinner("📡 Fetching Reddit data..."):
        scraped_data = scrape_user(username_input)
        if "error" in scraped_data:
            st.error(f"🚫 Reddit error: {scraped_data['error']}")
            st.stop()
        save_user_data(username_input, scraped_data)
        progress.progress(33)

    # Step 2: Cleaning
    with st.spinner("🔄 Processing data..."):
        cleaned = clean_user_data(scraped_data)
        save_cleaned_data(username_input, cleaned)
        progress.progress(66)

    # Step 3: Generating
    with st.spinner("🧠 Creating persona..."):
        persona_txt = generate_persona(username_input)
        progress.progress(100)
        time.sleep(0.5)
        progress.empty()

    # Success message with custom styling
    st.markdown("<div style='padding: 1rem; background-color: #1E4620; color: #4CAF50; border-radius: 0.5rem; margin: 1rem 0;'>✨ Persona Generated Successfully!</div>", unsafe_allow_html=True)

    # Display persona card
    st.markdown("<div class='persona-card'>", unsafe_allow_html=True)
    
    # Header with user info and avatar
    col1, col2 = st.columns([2, 3])
    with col1:
        # Generate and display avatar
        avatar_url = generate_avatar_url(persona_txt)
        st.image(avatar_url, width=500)
        st.markdown(f"<h2 style='text-align: center; color: #ff4500;'>u/{username_input}</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown(persona_txt)

    st.markdown("</div>", unsafe_allow_html=True)

    # Download option
    with open(f"data/personas/{username_input}_persona.txt", "rb") as f:
        st.download_button(
            label="📄 Download as Text",
            data=f,
            file_name=f"{username_input}_persona.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit + LLMs"
        "</div>",
        unsafe_allow_html=True
    )
