import os
from flask import Flask, flash, request, redirect, render_template,url_for
from resume_rating import file_constants as cnst
from resume_rating import resume_matcher
from resume_rating import file_utils
from Resume_Screening import resume_classifier
from flask import make_response


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg','docx'])
app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = cnst.UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/classify')
def classify():
    return render_template('resume_classifier.html')

@app.route('/rating')
def rating():
    return render_template('resume_loader.html')

@app.route('/failure')
def failure():
   return 'No files were selected'

@app.route('/success/<name>')
def success(name):
   return 'Files %s has been selected' %name

@app.route('/classify', methods=['POST', 'GET'])
def classes():
    if request.method == 'POST':        
        # check if the post request has the file part
        if 'resume_files' not in request.files:
           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        print(request.files)
        
        # resume_files = request.files['resume_files']
        # return render_template('resume_classifier.html')
        resume_files = request.files.getlist("resume_files")
        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)
        if ((len(resume_files) > 0)):
            #filename = secure_filename(file.filename)
            abs_paths = []

            for resumefile in resume_files:
                filename = resumefile.filename

                abs_paths.append(cnst.UPLOAD_FOLDER + '\\' + filename)
                resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            result = resume_classifier.process_files(abs_paths)
            for file_path in abs_paths:
                file_utils.delete_file(file_path)
            
            return render_template("resume_classes.html", result=result)
    return 'OK'

@app.route('/rating', methods=['POST', 'GET'])
def check_for_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'reqFile' not in request.files:
           flash('Requirements document can not be empty')
           return redirect(request.url)
        if 'resume_files' not in request.files:
           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        print(request.files)
        file = request.files['reqFile']
        if file.filename == '':
           flash('Requirement document has not been selected')
           return redirect(request.url)
        resume_files = request.files.getlist("resume_files")
        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)
        if ((file and allowed_file(file.filename)) and (len(resume_files) > 0)):
           #filename = secure_filename(file.filename)
           abs_paths = []
           filename = file.filename
           req_document = cnst.UPLOAD_FOLDER+'\\'+filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           for resumefile in resume_files:
               filename = resumefile.filename
               abs_paths.append(cnst.UPLOAD_FOLDER + '\\' + filename)
               resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
           result = resume_matcher.process_files(req_document,abs_paths)
           for file_path in abs_paths:
               file_utils.delete_file(file_path)

           return render_template("resume_results.html", result=result)
        else:
           flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
           return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True)