# Business Card Data Extractor✉️

## Overview

The **Business Card Data Extractor** is a simple and effective tool built using **Streamlit** that allows users to upload images of business cards and extract relevant contact details using a **vision-based Large Language Model (LLM)**. The extracted data is then stored in a CSV file for easy access and use.

This tool uses the **LangChain API** with the `llama-3.2-11b-vision-preview` model to process the uploaded images and extract the following details from the business card:
- Name
- Job Title
- Company
- Email
- Phone
- Website
- Address
![Screenshot 2025-02-01 123018](https://github.com/user-attachments/assets/3ace8a79-373c-4f6a-bc36-5d996a8219d7)
![2](https://github.com/user-attachments/assets/bf2b7bf8-d8c1-45d8-963d-5b70517db947)



## Features
- **Image Upload**: Users can upload business card images in formats like JPG, JPEG, or PNG.
- **Data Extraction**: The system uses an AI model to extract business card details in a structured JSON format.
- **CSV Storage**: Extracted data is saved into a CSV file to ensure persistence.

## Technologies Used
- **Streamlit**: For creating the interactive web application.
- **LangChain**: A framework for integrating large language models, used here to invoke the LLM for image-based data extraction.
- **Groq API**: For accessing the vision model (Llama 3.2) used to analyze business card images.
- **Python**: The core language used for implementing the logic.
