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

def is_baby_image(image_data):
    """
    Placeholder function to determine if the uploaded image is of a 0 to 2-month-old baby.
    You'll need to replace this with actual logic using an image classification model.
    """
    # Implement your classification model here
    # For the purpose of this example, it always returns True
    return True

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
st.title('Caritas de Bebé con OpenAI DALL-E 3')
st.write('Suba una imagen y escriba un prompt para editar la imagen con DALL-E 3.')

# Upload the image
uploaded_image = st.file_uploader("Suba la imagen...", type=["jpg", "jpeg", "png"])
prompt = st.text_input("Ingrese su prompt para editar:", "")

# Display the original image
if uploaded_image is not None:
    st.image(uploaded_image, caption='Imagen Original', use_column_width=True)

# Process the image when the user clicks the 'Edit Image' button
if st.button('Editar Imagen') and uploaded_image and prompt:
    # Read the uploaded image
    image_bytes = uploaded_image.getvalue()
    
    # Check if the image is of a baby in the specified age range
    if is_baby_image(image_bytes):
        # Edit the image
        edited_img = edit_image_with_prompt(image_bytes, prompt)
        
        # Display the edited image
        st.image(edited_img, caption='Imagen Editada', use_column_width=True)
    else:
        st.error("Lo siento, solo generamos caritas de bebés de 0 a 2 meses.")
