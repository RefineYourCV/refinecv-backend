import requests
import fitz  # PyMuPDF
from io import BytesIO
import pymupdf4llm
# def read_pdf_from_url(signed_url, filetype):
#     response = requests.get(signed_url)
#     response.raise_for_status()  # fail if not 200

#     # Load PDF into PyMuPDF
#     content = ""
#     with fitz.open(stream=BytesIO(response.content), filetype=filetype) as document:
#         for page in document:
#             content+= page.get_text("markdown")
            
#     return content


def read_pdf_from_url(signed_url, filetype):
    # Step 1: Download the PDF content from the signed URL
    response = requests.get(signed_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Step 2: Load the PDF into a PyMuPDF Document from the byte stream
    pdf_stream = BytesIO(response.content)
    with fitz.open(stream=pdf_stream, filetype=filetype) as doc:
        # Step 3: Extract Markdown using pymupdf4llm
        markdown_text = pymupdf4llm.to_markdown(doc)

    # Step 4: Return the extracted Markdown text
    return markdown_text

