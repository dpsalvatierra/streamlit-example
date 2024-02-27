import streamlit as st
from openai import AzureOpenAI
import os
import requests
from PIL import Image
from io import BytesIO
import base64

# Initialize the OpenAI API client
client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint="https://dalleai3.openai.azure.com/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# Function to send image edit requests to OpenAI
def edit_image_with_prompt(image_data, prompt):
    ''' Edit an image based on a textual prompt using OpenAI's DALL-E 3.'''
    image_b64 = base64.b64encode(image_data).decode('utf-8')

    response = client.images.edit(
        model="Dalle3",
        image=image_b64,
        prompt=prompt,
    )

    # Assuming the response has a direct link to the image
    image_url = response['data']['url']
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

# Streamlit app layout
st.title('DALL-E 2 Image Editor')
st.write('Upload an image and enter a prompt to edit it.')

# Upload the image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
prompt = st.text_input("Enter your edit prompt:", "")

# Display the original image
if uploaded_image is not None:
    st.image(uploaded_image, caption='Original Image', use_column_width=True)

# Process the image when the user clicks the 'Edit Image' button
if st.button('Edit Image') and uploaded_image and prompt:
    # Read the uploaded image
    image_bytes = uploaded_image.getvalue()
    
    # Edit the image
    edited_img = edit_image_with_prompt(image_bytes, prompt)
    
    # Display the edited image
    st.image(edited_img, caption='Edited Image', use_column_width=True)
