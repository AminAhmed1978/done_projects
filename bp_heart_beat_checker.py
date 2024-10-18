import streamlit as st
from transformers import pipeline
from PIL import Image
import concurrent.futures

# Load the depth estimation pipeline from Hugging Face with caching
@st.cache(allow_output_mutation=True)
def load_model():
    return pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")

depth_estimation_model = load_model()

def resize_image(image, max_size=512):
    width, height = image.size
    scaling_factor = min(max_size / width, max_size / height)
    new_size = (int(width * scaling_factor), int(height * scaling_factor))
    return image.resize(new_size, Image.LANCZOS)  # Updated to Image.LANCZOS

def async_depth_estimation(image):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(depth_estimation_model, image)
        return future.result()

def main():
    st.title("Heart Rate and Depth Estimation using Camera")

    st.sidebar.radio("Choose your role:", ("Admin", "Consumer"))

    st.subheader("Take a Photo for Analysis")
    st.text("Use your mobile or laptop camera to capture a clear image.")
    
    # Capture image using the webcam
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Captured Image', use_column_width=True)
        
        resized_image = resize_image(image)
        st.write("Analyzing the image...")
        
        # Perform depth estimation using asynchronous processing
        depth_result = async_depth_estimation(resized_image)
        st.write("Depth Estimation Result: ", depth_result)

        st.write("Heart Rate estimation would be calculated based on depth changes here.")

if __name__ == "__main__":
    main()
