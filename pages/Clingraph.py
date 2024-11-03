import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import textwrap

# Configure page settings
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize Gemini API
def initialize_gemini():
    try:
        api_key = st.secrets["XXX"]
    except:
        api_key = st.sidebar.text_input("Enter your Gemini API key:", type="password")
        if not api_key:
            st.info("Please enter your Gemini API key to continue.")
            st.stop()
    
    genai.configure(api_key=api_key)
    return genai

# Function to load Gemini Pro model for text
def load_gemini_pro():
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    return model

# Function to load Gemini Pro Vision model for images
def load_gemini_pro_vision():
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    return model

# Function to process text prompts
def process_text_prompt(prompt):
    model = load_gemini_pro()
    response = model.generate_content(prompt)
    return response.text

# Function to process image analysis
def process_image(image, prompt):
    model = load_gemini_pro_vision()
    response = model.generate_content([prompt, image])
    return response.text

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .upload-box {
        border: 2px dashed #cccccc;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Initialize Gemini
    genai = initialize_gemini()
    
    # App title and description
    st.title("🤖 Gemini AI Assistant")
    st.markdown("""
    This app demonstrates the capabilities of Google's Gemini AI for both text and image analysis.
    Choose your interaction mode below.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a mode:", ["Text Generation", "Image Analysis"])
    
    if page == "Text Generation":
        st.header("💭 Text Generation")
        st.markdown("Enter your prompt below and let Gemini generate text content for you.")
        
        # Text input section
        text_prompt = st.text_area("Enter your prompt:", height=100)
        
        if st.button("Generate"):
            if text_prompt:
                with st.spinner("Generating response..."):
                    try:
                        response = process_text_prompt(text_prompt)
                        st.markdown("### Response:")
                        st.markdown(response)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a prompt first.")
                
    else:  # Image Analysis page
        st.header("🖼️ Image Analysis")
        st.markdown("Upload an image and ask Gemini to analyze it.")
        
        # Image upload section
        uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image analysis prompt
            analysis_prompt = st.text_input(
                "What would you like to know about this image?",
                placeholder="E.g., 'Describe this image in detail' or 'What objects do you see?'"
            )
            
            if st.button("Analyze"):
                if analysis_prompt:
                    with st.spinner("Analyzing image..."):
                        try:
                            response = process_image(image, analysis_prompt)
                            st.markdown("### Analysis Results:")
                            st.markdown(response)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                else:
                    st.warning("Please enter an analysis prompt first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### Tips for best results:
    - For text generation, be specific and clear in your prompts
    - For image analysis, ensure good image quality and specific questions
    - API responses may vary based on the complexity of your request
    """)

if __name__ == "__main__":
    main()
