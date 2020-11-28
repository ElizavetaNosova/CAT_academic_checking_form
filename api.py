#import flask
import os
from flask import *
#import docx2pdf
#import docx

UPLOAD_FOLDER = 'student_texts'
ALLOWED_EXTENSIONS = {'txt', 'docx'}


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                     filename, as_attachment=True, 
                     #mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document') 
                     mimetype = 'content-type=text/plain; charset=utf-8')

@app.route('/upload_docx_file', methods=['POST'])
def upload_docx_file():
    file = request.files['file']
    
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('uploaded_file', filename=filename))
    #r = make_response(file)
    #r.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document; charset=utf-8'
    #return r

    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
        #	file_content = docx.Document(f)
    #file_text = '/n'.join([paragraph.text for paragraph in file_content.paragraphs])
    #file_text = 'ЗД'
    #return redirect(request.url)
    return redirect(url_for('uploaded_file', filename=filename))
# A route to return all of the available entries in our catalog.
#@app.route('/api/v1/resources/books/all', methods=['GET'])
#def api_all():
#    return jsonify(books)

app.run()