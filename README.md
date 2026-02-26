
[https://pptx2html-dashboard.streamlit.app/](https://pptx2html-dashboard.streamlit.app/)


# PPTX → HTML Dashboard

A simple Streamlit web app that converts PowerPoint (.pptx) files into a standalone HTML dashboard.

Upload a PPTX file and download a clean HTML version where each slide is rendered as an image inside a modern card-style layout.

---

## 🚀 Live Demo

[https://pptx2html-dashboard.streamlit.app/](https://pptx2html-dashboard.streamlit.app/)

---

## 🛠 How It Works

The conversion pipeline:

PPTX → (LibreOffice headless) → PDF → (pdf2image + Poppler) → PNG → Embedded in HTML

- LibreOffice converts PPTX to PDF
- pdf2image converts each PDF page to an image
- Images are embedded in a standalone HTML file using base64 encoding

The final HTML file requires no external assets — it works anywhere.

---