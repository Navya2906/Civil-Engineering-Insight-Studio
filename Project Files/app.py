import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
from google import genai


# ================================
# Activity 1: Load Environment
# ================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# ================================
# Activity 2: Gemini Response Function
# ================================

def get_gemini_response(input_text, image, prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # ✅ Guaranteed available
        contents=[input_text, image, prompt]
    )

    return response.text


# ================================
# Activity 3: Image Setup Function
# ================================

def input_image_setup(uploaded_file):

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        return image

    else:
        raise FileNotFoundError("No file uploaded")


# ================================
# Activity 4: Streamlit Web App
# ================================

st.set_page_config(
    page_title="Civil Engineering Insight Studio",
    page_icon="🏗️"
)

st.header("🏗️ Civil Engineering Insight Studio")


# Text input
input_text = st.text_input("📝 Input Prompt:", key="input")


# File uploader
uploaded_file = st.file_uploader(
    "📂 Choose an image...",
    type=["jpg", "jpeg", "png"]
)


# Display image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=600)


# Submit button
submit = st.button("🚀 Describe Structure")


# Prompt for Gemini
input_prompt = """
You are a civil engineering expert.

Analyze the uploaded image and provide a detailed description of the structure including:

1. Type of structure
2. Materials used
3. Dimensions (if possible)
4. Construction methods
5. Notable features or engineering challenges

Explain clearly and professionally.
"""


# ================================
# Process Input & Generate Output
# ================================

if submit:
    try:
        if uploaded_file is not None:

            image_data = input_image_setup(uploaded_file)

            response = get_gemini_response(
                input_text,
                image_data,
                input_prompt
            )

            st.subheader("📌 Description of the Civil Engineering Structure:")
            st.write(response)

        else:
            st.warning("⚠️ Please upload an image first.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
