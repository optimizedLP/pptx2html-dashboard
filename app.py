from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import os, subprocess, base64
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
ALLOWED_EXTENSIONS = {"pptx"}

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert PPTX to PDF using LibreOffice CLI
def pptx_to_pdf(pptx_path):
    pdf_filename = os.path.basename(pptx_path).replace(".pptx", ".pdf")
    pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)

    # Make sure LibreOffice is installed: soffice CLI
    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        pptx_path,
        "--outdir",
        OUTPUT_FOLDER
    ], check=True)

    return pdf_path

# Convert PDF to standalone HTML with embedded images
def pdf_to_html(pdf_path):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=150)  # Higher dpi = better quality

    # Start HTML content
    html_content = "<!DOCTYPE html>\n<html>\n<head>\n"
    html_content += "<title>PPTX Dashboard</title>\n"
    html_content += f'<link rel="stylesheet" href="{ url_for("static", filename="styles.css") }">\n'
    html_content += "</head>\n<body>\n"

    # Embed each slide as Base64 image
    for page in pages:
        img_bytes = BytesIO()
        page.save(img_bytes, format="PNG")
        encoded = base64.b64encode(img_bytes.getvalue()).decode()
        html_content += f'<img src="data:image/png;base64,{encoded}" class="slide-img">\n'

    html_content += "</body>\n</html>"

    # Save HTML
    html_filename = os.path.basename(pdf_path).replace(".pdf", "_dashboard.html")
    html_path = os.path.join(OUTPUT_FOLDER, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_filename

# Main page: upload PPTX
@app.route("/", methods=["GET", "POST"])
def index():
    html_file = None
    if request.method == "POST":
        if "pptx_file" not in request.files:
            return "No file part"
        file = request.files["pptx_file"]
        if file.filename == "":
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            # Convert PPTX → PDF
            pdf_path = pptx_to_pdf(save_path)

            # Convert PDF → standalone HTML
            html_file = pdf_to_html(pdf_path)

    return render_template("index.html", html_file=html_file)

# Serve generated HTML
@app.route("/output/<filename>")
def output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)