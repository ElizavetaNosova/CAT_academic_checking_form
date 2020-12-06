#import flask
import os
from flask import *
import spelling
import uuid 
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


def get_text(file_name):
    pass

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_id = uuid.uuid1().hex
    print('id type', type(file_id))
    file_name = file_id + '.' + file.filename.split('.')[-1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    if file.filename.split('.')[-1] != 'txt':
        file_text = get_text(file_name)
        txt_name = file_id + '.txt'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], txt_name))
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
    # file_name = file_id + '.txt'
    # with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), encoding='utf-8') as f:
    #     text = f.read()
    # spellchecker = spelling.SpellChecker()
    # try:
    #     spelling_problems = spellchecker.check_spelling(text)
    # except spelling.ParagraphLengthException:
    #     #придумать обработку исключения
    #     spelling_problems = []
    return jsonify({'spelling_problems': check_spelling(file_id)})

@app.route('/correct_spelling', methods=['POST'])
def correct_spelling():
    # corrections = request.json
    # #написать проверку входных данных
    # file_name = corrections['file_id'] + '.txt'
    # new_file_name = corrections['new_file_id'] + '.txt'
    # spelling_problems = corrections['spelling_problems']
    # with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), encoding='utf-8') as f:
    #     text = f.read()
    # corrected_text = spelling.make_changes(text, spelling_problems)
    # with open(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name), encoding='utf-8') as f:
    #     f.write(corrected_text)
    print(request.json)
    return json.dumps({'success':True}), 200
    


    #return redirect(url_for('uploaded_file', filename=filename))
   
# A route to return all of the available entries in our catalog.
#@app.route('/api/v1/resources/books/all', methods=['GET'])[]
#    return jsonify(books)


app.run()