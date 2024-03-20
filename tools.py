import streamlit as st
import pytesseract
from PIL import Image
#pip install fitz
#pip install frontend
import fitz
import os
from docx import Document

# Function to extract text from image using pytesseract
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text


def pdf_to_document(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Create a new Word document
    docx_document = Document()
    docx_document.add_paragraph(text)

    # Save the document
    docx_document.save(output_path)

    return output_path



# Function to extract code from image
def extract_code_from_image(image):
    # You'll need to implement this function based on your specific requirements
    # It might involve OCR techniques and code parsing
    pass

def main():
    st.title("Document Processing App")

    st.sidebar.header("Options")
    task = st.sidebar.selectbox("Choose a task", ("Extract Text from Image", "PDF to Document", "Extract Code from Image"))

    if task == "Extract Text from Image":
        st.subheader("Extract Text from Image")
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            text = extract_text_from_image(image)
            st.write("Extracted Text:")
            st.write(text)
    elif task == "PDF to Document":
        st.subheader("PDF to Document")
        uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

        if uploaded_pdf is not None:
            with st.spinner('Converting PDF to Document...'):
                # Save the uploaded PDF to a temporary location
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_pdf.read())
                
                # Convert the uploaded PDF to a document
                output_path = "output_document.txt"
                output_path = pdf_to_document("temp.pdf", output_path)
                
                # Display a success message
                st.success(f"Document created at {output_path}")

                # Remove the temporary PDF file
                os.remove("temp.pdf")

                # Add a download button for the converted document
                st.download_button(
                    label="Download Document",
                    data=output_path,
                    file_name="output_document.txt",
                    mime="text/plain"
                )


if __name__ == "__main__":
    main()
