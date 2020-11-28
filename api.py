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


@app.route('/aspect_form', methods=['GET'])
def render_aspect_form():
    return render_template('aspect_form.html')    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                     filename, as_attachment=True, 
                     #mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document') 
                     mimetype = 'content-type=text/plain; charset=utf-8')

@app.route('/spelling_form')
def render_spelling_form():
    return render_template('spelling_form.html')

def get_id():
    return '4'

def convert_into_txt(file_name):
    pass

@app.route('/upload_docx_file', methods=['POST'])
def upload_docx_file():
    file = request.files['file']
    file_id = get_id() 
    file_name = file_id + '.' + file.filename.split('.')[-1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    if file.filename.split('.')[-1] != 'txt':
        convert_into_txt(file_name)
    return jsonify({'file_id': file_id})

def check_spelling(file_id):
    return [{'code': 1,
  'pos': 456,
  'row': 1,
  'col': 440,
  'len': 15,
  'word': 'распостроняется',
  's': ['распространяется', 'распостраняется', 'распростроняется'],
  'problem_type': 'spelling',
  'text': 'подвиргаются',
  'end': 471,
  'context': 'ЗДЕСЬ БУДЕТ КОНТЕКСТ'},
 {'code': 1,
  'pos': 550,
  'row': 1,
  'col': 534,
  'len': 12,
  'word': 'подвиргаются',
  's': ['подвергаются'],
  'problem_type': 'spelling',
  'end': 562,
  'context': 'ЗДЕСЬ БУДЕТ КОНТЕКСТ'}]

@app.route('/get_spelling_problems/<file_id>', methods=['GET'])
def get_spelling_data(file_id):
    return jsonify({'spelling_problems': check_spelling(file_id)})


    #return redirect(url_for('uploaded_file', filename=filename))
   
# A route to return all of the available entries in our catalog.
#@app.route('/api/v1/resources/books/all', methods=['GET'])[]
#    return jsonify(books)


app.run()