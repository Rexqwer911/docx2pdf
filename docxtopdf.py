from flask import Flask, request, Response
import subprocess
import shutil
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():

    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']

    if not file.filename.endswith('.docx'):
        return "Invalid file format. Only .docx files are supported", 400

    unique_folder_name = str(uuid.uuid4())
    uuid_folder_path = os.path.join(UPLOAD_FOLDER, unique_folder_name)

    os.makedirs(uuid_folder_path, exist_ok=True)

    filename = str(file.filename)

    input_path = os.path.join(uuid_folder_path, filename)
    print(str(input_path))
    file.save(input_path)

    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path, '--outdir', uuid_folder_path], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}", 500

    pdf_filename = filename.replace('.docx', '.pdf')
    with open(os.path.join(uuid_folder_path, filename.replace('.docx', '.pdf')), 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    shutil.rmtree(uuid_folder_path)

    return Response(pdf_data, mimetype='application/pdf', headers={'Content-Disposition': f'attachment; filename={pdf_filename}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)