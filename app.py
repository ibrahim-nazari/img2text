from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
import requests
import os
import streamlit as st
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
            with open("audio.flac","wb") as file:
                file.write(response.content)
        except Exception as e:
                print(f"An error occurred: {e}")

 

    
def main():
     st.set_page_config(page_title="image to text, and text into audio ",page_icon="🍒")
     st.header("Turn image to text, and text into audio ")
     uploaded_file=st.file_uploader("Choose an image ...")

     if uploaded_file is not None:
            print(uploaded_file)
            bytes_data=uploaded_file.getvalue()
            with open(uploaded_file.name,"wb") as file:
                file.write(bytes_data)
            st.image(uploaded_file,caption="uploaded image.",use_column_width=True)
            story=image2text(uploaded_file.name)
            text=story[0]["generated_text"]
            text2speach(text)
            with st.expander("Story"):
                 st.write(text)
            st.audio("audio.flac")




if __name__ =="__main__":
     main()
          
       