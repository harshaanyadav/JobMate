
JobMate - Resume Analyzer & Personality Insights

JobMate is a desktop Python application that extracts text from resumes (PDFs), parses the content, performs basic analysis, and optionally predicts personality traits. It provides a GUI built with tkinter, integrates resume parsing, data visualization, and interaction with LinkedIn or other platforms.

⸻

Features
	•	PDF Resume Parsing using pdfplumber
	•	Text Analysis with re, pandas, numpy
	•	Visualizations using matplotlib
	•	Personality Prediction (based on keywords or NLP, if implemented)
	•	Screenshot and Image Handling with PIL
	•	LinkedIn Integration for profile viewing
	•	GUI using tkinter, ttk, and ScrolledText
	•	File import/export functionality with user-friendly dialogs

⸻

Technologies Used
	•	Python 3.x
	•	pdfplumber
	•	pandas
	•	matplotlib
	•	Pillow (PIL)
	•	numpy
	•	tkinter (built-in)

⸻

Getting Started

Prerequisites

Make sure Python 3.10 or above is installed. You can check with:

python3 --version

Install dependencies:

pip install -r requirements.txt

If you don’t have requirements.txt, here’s how to generate one:

pip freeze > requirements.txt



Running the App

python3 main.py

The GUI will launch allowing you to upload PDF resumes and interact with various features.

⸻

Project Structure

JobMate/
├── main.py             # Main GUI application
├── requirements.txt    # List of required packages
├── assets/             # Any icons, images (optional)
└── README.md           # Project documentation


⸻

Authentication & LinkedIn

The app may attempt to open web profiles using webbrowser — make sure you’re connected to the internet and logged into your browser for smooth interaction.

⸻

Screenshots

(Include a screenshot here once available to showcase the UI)

⸻

License

This project is licensed under the MIT License — feel free to modify and use it.
