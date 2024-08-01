from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
import io
import time
import re

app = Flask(__name__)

client = Groq(
    api_key='your api key here',
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_outline', methods=['POST'])
def generate_outline():
    subject = request.json.get('subject')
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate an outline for an essay on the subject: {subject}"}
        ]
    )

    outline = response.choices[0].message.content.strip()
    return jsonify({'outline': outline})

@app.route('/generate_essay', methods=['POST'])
def generate_essay():
    outline = request.json.get('outline')
    sections = extract_sections(outline)
    essay = ""
    references = []

    for section in sections:
        prompt = (
            "For an academic level paper, adhere to these guidelines:\n"
            "- Write like a human.\n"
            "- Maintain a scholarly tone with high-level academic language and style.\n"
            "- Avoid redundancy by exploring different aspects of your argument.\n"
            "- Write detailed, logically structured paragraphs.\n"
            "- Use transitional phrases to enhance argument flow.\n"
            "- Employ varied sentence structures to create rhythm and balance.\n"
            "- Enrich writing with diverse, academic vocabulary.\n"
            "- Ensure a coherent, cohesive argument, each point building upon the last.\n"
            "- Engage critically with the topic, analyzing and evaluating different viewpoints.\n"
            "- Avoid awkward phrasing; ensure sentences are grammatically correct and precise.\n"
            "- Avoid repetitive expressions and refrain from rehashing ideas already discussed in your previous responses.\n"
            "- Avoid using meta-commentary and instructional notes.\n\n"
            f"- By following the guidelines above, in one long paragraph, write the:\n{section}\n\n"
            "**NOTE: use only one real external source, cite it correctly and give the full reference at the end."
        )

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        paragraph = response.choices[0].message.content.strip()
        
        # Extract and remove reference
        reference_match = re.search(r'References?:\s*(.*)', paragraph, re.IGNORECASE)
        if reference_match:
            references.append(reference_match.group(1).strip())
            paragraph = re.sub(r'References?:\s*.*', '', paragraph, flags=re.IGNORECASE).strip()
        
        # Remove meta-commentary and instructional notes
        paragraph = re.sub(r"^(Note:.*|Here is the.*|Here's the.*|Here's a.*|Here is a.*|Please.*)$", '', paragraph, flags=re.MULTILINE).strip()

        essay += f"{paragraph}\n\n"
        
        time.sleep(1)  # To avoid hitting rate limits

    # Combine references
    if references:
        essay += "References:\n" + "\n\n".join(references)

    return jsonify({'essay': essay})

@app.route('/download_docx', methods=['POST'])
def download_docx():
    data = request.json
    essay_text = data['essay']

    doc = Document()
    doc.add_paragraph(essay_text)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='essay.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.json
    essay_text = data['essay']

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica", 12)

    text_object = p.beginText(40, height - 40)
    lines = essay_text.split('\n')
    for line in lines:
        wrapped_lines = utils.simpleSplit(line, "Helvetica", 12, width - 80)
        for wrapped_line in wrapped_lines:
            text_object.textLine(wrapped_line)
            if text_object.getY() < 40:
                p.drawText(text_object)
                p.showPage()
                text_object = p.beginText(40, height - 40)
                text_object.setFont("Helvetica", 12)
    p.drawText(text_object)
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='essay.pdf', mimetype='application/pdf')

def extract_sections(outline):
    lines = outline.split('\n')
    sections = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Note:"):
            continue
        
        if line.startswith("*") or line.startswith("+"):
            current_section += f"\n{line.lstrip('*+').strip()}"
        else:
            if current_section:
                sections.append(current_section.strip())
            current_section = line.strip()

    if current_section:
        sections.append(current_section.strip())

    return sections

if __name__ == '__main__':
    app.run(debug=True)
