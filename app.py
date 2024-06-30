from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
import requests
import os
import streamlit as st
from PIL import Image
HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}

def image2text(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()



 


def text2speach(text):
        try:
            API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
            headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
            response = requests.post(API_URL, headers=headers, json={"inputs":text})
            with open("data/audio.flac","wb") as file:
                file.write(response.content)
        except Exception as e:
                print(f"An error occurred: {e}")

 
def imgResize(name):
    
    this_image = Image.open(f"data/{name}")
    width, height = this_image.size
    TARGET_WIDTH = 500
    coefficient = width / 500
    new_height = height / coefficient
    this_image = this_image.resize((int(TARGET_WIDTH),int(new_height)),Image.Resampling.LANCZOS)
    this_image.save(f"data/{name}",quality=50)

         

    
def main():
     st.set_page_config(page_title="image to text, and text into audio ",page_icon="🍒")
     st.header("Turn image to text, and text into audio ")
     uploaded_file=st.file_uploader("Choose an image ...")

     if uploaded_file is not None:
            print(uploaded_file)
            bytes_data=uploaded_file.getvalue()
            with open(f"data/{uploaded_file.name}","wb") as file:
                file.write(bytes_data)
            imgResize(uploaded_file.name)
            st.image(uploaded_file,caption="uploaded image.",use_column_width=True)
            story=image2text(f"data/{uploaded_file.name}")
            text=story[0]["generated_text"]
            text2speach(text)
            with st.expander("Text interpretation"):
                 st.write(text)
            st.audio(f"data/audio.flac")




if __name__ =="__main__":
     main()
          
       