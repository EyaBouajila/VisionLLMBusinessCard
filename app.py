import streamlit as st
import base64
import json
import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("vision_api")

# Initialize LLM model
llm = ChatGroq(
    model_name="llama-3.2-11b-vision-preview",
    temperature=0,
    groq_api_key=API_KEY
)

# Define CSV file path (persistent location)
CSV_FILE = "C:\\Users\\eya\\PycharmProjects\\BusinessCardLLM\\business_cards.csv"

# Ensure session state for extracted data
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

def extract_business_card_data(image_base64):
    prompt_text = """Extract contact details from this business card image and return the result as JSON. Ensure the response contains only valid JSON; NO explanations. NO PREAMBULE.
    Example format:
    {
        "Name": "John Doe",
        "Job Title": "Software Engineer",
        "Company": "TechCorp",
        "Email": "john.doe@example.com",
        "Phone": "123-456-7890",
        "Website": "www.techcorp.com",
        "Address": "123 Main St, City, Country"
    }
    """
    response = llm.invoke([
        HumanMessage(content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ])
    ])

    # Extract the JSON part from the response
    try:
        json_start = response.content.find("{")
        json_data = response.content[json_start:]
        extracted_data = json.loads(json_data)
    except json.JSONDecodeError:
        st.error("Failed to parse extracted data. Please try again.")
        extracted_data = {}

    return extracted_data

def save_to_csv(data, filename=CSV_FILE):
    fields = ["Name", "Job Title", "Company", "Email", "Phone", "Website", "Address"]
    business_card_data = {field: data.get(field, "N/A") for field in fields}

    try:
        # Check if file exists, append if yes, create if no
        file_exists = os.path.exists(filename)

        with open(filename, mode="a", newline="", encoding="utf-8") as f:
            df = pd.DataFrame([business_card_data])
            df.to_csv(f, header=not file_exists, index=False)

        st.success(f"Data successfully saved")

    except Exception as e:
        st.error(f"Error saving file: {e}")

# Streamlit UI
st.title("Business Card Data Extractor")

uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Convert image to base64
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Business Card", use_container_width=True)

    # Extract Data Button
    if st.button("Extract Data"):
        with st.spinner("Extracting data..."):
            extracted_data = extract_business_card_data(image_base64)
            st.session_state.extracted_data = extracted_data  # Store in session state
            st.json(extracted_data)

# Ensure extracted data persists until saved
if st.session_state.extracted_data:
    if st.button("Save to CSV"):
        save_to_csv(st.session_state.extracted_data)
