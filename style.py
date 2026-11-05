"""Custom CSS styling for RecallBuddy Streamlit app."""

import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #B4FF39;
            font-family: 'Arial', sans-serif;
        }

        /* Force ALL text in the app to be readable (black/dark gray).
           Badges and explicitly-colored elements keep their colors. */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp p, .stApp li, .stApp label, .stApp div, .stApp span,
        .stApp a, .stApp small, .stApp strong, .stApp em,
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {
            color: #000000 !important;
        }

        /* White cards: solid white background, black border, padding, radius */
        .white-card {
            background-color: #FFFFFF;
            border: 3px solid #000000;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 4px 4px 0px #000000;
        }

        /* Hero headline: black, bold, uppercase */
        .hero-title {
            font-size: 3rem;
            font-weight: 900;
            line-height: 1.1;
            text-transform: uppercase;
            color: #000000;
        }

        .hero-sub {
            font-size: 1rem;
            color: #000000;
        }

        /* Buttons: black background, black text for readability */
        .stButton > button {
            background-color: #000000;
            color: #000000;
            border-radius: 50px;
            padding: 10px 24px;
            border: 2px solid #000000;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #333333;
            color: #FFFFFF;
            border: 2px solid #B4FF39;
        }

        /* Radio buttons: white background, black text */
        .stRadio > div {
            background-color: #FFFFFF;
            border-radius: 8px;
            padding: 4px;
        }
        .stRadio label {
            color: #000000 !important;
        }
        .stRadio [role="radio"] {
            accent-color: #000000;
        }

        /* Text inputs: white background, black text */
        .stText input {
            background-color: #FFFFFF;
            color: #000000;
            border: 2px solid #000000;
        }
        .stText input::placeholder {
            color: #666666;
        }

        /* Badges keep their styling (black bg, white text) */
        .badge {
            background: #000000;
            color: #FFFFFF;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }

        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )