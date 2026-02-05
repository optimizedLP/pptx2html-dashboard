# PPTX to HTML Dashboard

Convert your PowerPoint (.pptx) slides into a visually appealing HTML dashboard. Upload a PPTX, preview slides in your browser, and download a standalone HTML file that works offline.

**Live Demo:** [https://pptx2html-dashboard.onrender.com](https://pptx2html-dashboard.onrender.com)

## Features

- Upload PPTX files in the browser
- Preview slides as dashboard-style images
- Download a self-contained HTML dashboard
- No Python knowledge required

## How to Run Locally

Clone the repo and enter the folder:  
`git clone https://github.com/<yourusername>/pptx-to-html-dashboard.git`  
`cd pptx-to-html-dashboard`

Create a virtual environment and install dependencies:  
`python -m venv venv`  
`source venv/bin/activate`  (Mac/Linux)  
`venv\Scripts\activate`     (Windows)  
`pip install -r requirements.txt`

Run the app:  
`python app.py`

Open your browser at `http://127.0.0.1:5000` and upload a PPTX file.

## Notes

- Uploaded PPTX files and generated dashboards are temporarily stored in `uploads/` and `output/`.  
- Downloaded HTML files are fully self-contained and work offline.
