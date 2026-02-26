import streamlit as st
import os
import subprocess
import base64
import tempfile
from pdf2image import convert_from_path
from io import BytesIO

st.set_page_config(page_title="PPTX → HTML Dashboard", layout="centered")

st.title("PPTX → HTML Dashboard")
st.write("Upload a PPTX file and convert it into a HTML dashboard.")

ALLOWED_EXTENSIONS = {"pptx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert PPTX → PDF
def pptx_to_pdf(pptx_path, output_dir):
    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        pptx_path,
        "--outdir",
        output_dir
    ], check=True)

    pdf_name = os.path.basename(pptx_path).replace(".pptx", ".pdf")
    return os.path.join(output_dir, pdf_name)

# Convert PDF → standalone HTML
def pdf_to_html(pdf_path, output_dir):
    pages = convert_from_path(pdf_path, dpi=150)

    html = """<!DOCTYPE html>
<html>
<head>
<title>PPTX Dashboard</title>
<style>
body { font-family: Arial; background: #fafafa; }
.slide-img { width: 100%; margin-bottom: 20px; }
</style>
</head>
<body>
"""

    for page in pages:
        buf = BytesIO()
        page.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode()
        html += f'<img src="data:image/png;base64,{encoded}" class="slide-img"/>\n'

    html += "</body></html>"

    html_path = os.path.join(output_dir, "dashboard.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html_path

# UI: File upload
uploaded_file = st.file_uploader("Upload PPTX file", type=["pptx"])

if uploaded_file:
    if not allowed_file(uploaded_file.name):
        st.error("Invalid file type")
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            pptx_path = os.path.join(tmpdir, uploaded_file.name)
            with open(pptx_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success("File uploaded")

            with st.spinner("Converting PPTX → PDF → HTML..."):
                pdf_path = pptx_to_pdf(pptx_path, tmpdir)
                html_path = pdf_to_html(pdf_path, tmpdir)

            st.success("Conversion complete!")

            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            st.download_button(
                label="Download HTML Dashboard",
                data=html_content,
                file_name="dashboard.html",
                mime="text/html"
            )