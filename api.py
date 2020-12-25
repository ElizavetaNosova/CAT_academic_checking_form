#import flask
import os
from flask import *
import spelling
import uuid



def dummy_morphology_checker(text):
    return []

def dummy_duplicates_checker(text):
    return []

UPLOAD_FOLDER = 'student_texts'
ALLOWED_EXTENSIONS = {'txt'}
ASPECTS =  [{'id': 'morphology','russian': 'Словоформы, не представленные в CAT'},
           {'id': 'duplicates','russian': 'Повторы'}]
ASPECT2FUNCTION  = {
    'morphology': dummy_morphology_checker,
    'duplicates': dummy_duplicates_checker
}


def save_file_first_time_and_get_id(file):
    text_id = uuid1().hex
    txt_name = text_id + '_version_0.txt'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], txt_name))
    return text_id

def save_text_first_time_and_get_id(text):
    text_id = uuid1().hex
    txt_name = text_id + '_version_0.txt'
    with open(os.path.join(app.config['UPLOAD_FOLDER'], txt_name), 'w', encoding='utf-8') as f:
        f.write(text)
    return text_id

def save_next_version(text, text_id):
    upload_folder = app.config['UPLOAD_FOLDER']
    all_saved_student_texts = os.listdit(upload_folder)
    current_text_versions = [filename for filename in all_saved_student_texts if filename.startsWith(text_id + '_version')]
    next_version_filename = text_id + '_version_' + str(len(current_text_versions))  + '.txt'
    with open(os.path.join(app.config['UPLOAD_FOLDER'], next_version_filename), 'w', encoding='utf-8') as f:
        f.write(text)

def get_last_version(text_id):
    upload_folder = app.config['UPLOAD_FOLDER']
    all_saved_student_texts = os.listdit(upload_folder)
    current_text_versions = [filename for filename in all_saved_student_texts if filename.startsWith(text_id + '_version')]
    if (current_text_versions):
        last_version_filename = text_id + '_version_' + str(len(current_text_versions)-1) + '.txt'
        with open(os.path.join(app.config['UPLOAD_FOLDER'], next_version_filename), encoding='utf-8') as f:
            text = f.read()
            return text
    else:
        return ''



app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ASPECT2FUNCTION"] = ASPECT2FUNCTION
app.config["ASPECTS"] = ASPECTS


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
    text_id = save_file_first_time_and_get_id()
    file_name = text_id + '_version_0.txt'
    return jsonify({'file_id': file_id})

def check_spelling(text_id):
    text = get_last_version(text_id)
    spellchecker = spellching.SpellChecker()
    problems = spellchecker.check_spelling(text)['problems']
    return problems


@app.route('/get_spelling_problems/<file_id>', methods=['GET'])
def get_spelling_data(file_id):
    return jsonify({'spelling_problems': check_spelling(file_id)})

@app.route('/correct_spelling', methods=['POST'])
def correct_spelling()
    return json.dumps({'success':True}), 200

@app.route('/possible_aspects', methods=['GET'])
def possible_aspects():
    ##Сюда добавить английский вариант, будем делать английскую версию

    ##Переписать функцию, если будут аспекты, которые доступны не всегда
    possible_aspects = [{'id': 'morphology','russian': 'Словоформы, не представленные в CAT'},
                        {'id': 'duplicates','russian': 'Повторы'}]
    return jsonify({'possible_aspects': possible_aspects})





    #return redirect(url_for('uploaded_file', filename=filename))

# A route to return all of the available entries in our catalog.
#@app.route('/api/v1/resources/books/all', methods=['GET'])[]
#    return jsonify(books)

if __name__ == '__main__':
    app.run()
