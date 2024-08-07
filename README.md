# Free Essay Generator

This web application generates an essay outline and a full essay based on a given subject, with GroqCloud API to generate content using llama3-8b-8192 model. It also allows saving the generated essay as a DOCX or PDF file.

## Features

- Generate an essay outline from a provided subject
- Generate a full essay based on the outline
- Save the generated essay as a DOCX file
- Save the generated essay as a PDF file
- Friendly web design

## Technologies Used

- Python (Flask) for the backend
- JavaScript for frontend interactions
- HTML/CSS for the frontend design
- ReportLab for PDF generation
- python-docx for DOCX generation

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/obaskly/Essay-Generator.git
    cd Essay-Generator
    ```

2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

### API set up

- Get your free api from here https://console.groq.com/keys and place it in line 14 in app.py

### Running the Application

1. Start the Flask server:
    ```
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

### Usage

1. Enter a subject in the input box and click "Continue" to generate an outline.
2. Review and modify the generated outline if necessary.
3. Click "Generate Essay" to create a full essay based on the outline.
4. Save the essay by clicking "Save as DOCX" or "Save as PDF".

## File Structure

- `app.py`: Main Flask application file.
- `templates/index.html`: HTML template for the web interface.
- `static/styles.css`: CSS styles for the web interface.
- `requirements.txt`: List of Python packages required for the project.

## TODO

- The script now generates references and places them at the end. But sometimes they are still between paragraphs. I'll improve that later.
