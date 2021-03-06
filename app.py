
from crypt import methods
from fileinput import filename
import os
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap5 import Bootstrap
import PyPDF2



app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/Users/dn/Documents/GitHub/ISD_Project2/static/resume_uploads"
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
bootstrap = Bootstrap(app)

user = {}


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/upload.html', methods = ['GET', 'POST'])
def upload():
        print("inuploads")
        
        if request.method == "GET":
           print("posted!")
           if request.files:
               print("file requested")
               file = request.files["filename"]
               
               file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
               print(file)
               return redirect(request.url)
        
        return render_template('upload.html')



@app.route('/display.html', methods=['POST'])
def display():
    if request.method == 'POST' and 'filename' in request.files \
            and request.files['filename'].content_type == 'application/pdf':
        file = request.files['filename']
        
        
        
        pdfReader = PyPDF2.PdfFileReader(file)

        # Getting number of pages in pdf fileF
        pages = pdfReader.numPages
        # Loop for reading all the Pages
        for i in range(pages):
            # Creating a page object
            pageObj = pdfReader.getPage(i)
            # Printing Page Number
            print("Page No: ", i)
            # Extracting text from page
            # And splitting it into chunks of lines
            text = pageObj.extractText().split('\n')
            # Finally the lines are stored into list
            # For iterating over list a loop is used

            # the join function joins the strings together so
            # ''.join(text[5:9]) is effectively the same as
            # text[5]+text[6]+text[7]+text[8]
            user['name'] = ''.join(text[5:9])
            user['address'] = ''.join(text[10:13])
            user['phone_number'] = ''.join(text[14:17])
            user['email'] = text[18]
            user['qualifications'] = ''.join(text[23:36])
            user['education'] = ''.join(text[40:54])
            user['accomplishments'] = ''.join(text[58:106])
            user['work_history'] = ''.join(text[110:132])
            user['professional_affiliation'] = ''.join(text[136:139])
            user['computer_skills'] = ''.join(text[146:151])

            '''
            for j in range(len(text)):
                # Printing the line
                # Lines are separated using "\n"
                print("page #" + str(j) + ": " + text[j], end="\n")
                # For Separating the Pages
            '''

        print("file sent successfully")
        return render_template("display.html", name=user['name'], address=user['address'],
                               phone_number=user['phone_number'], email=user['email'],
                               qualifications=user['qualifications'], education=user['education'],
                               accomplishments=user['accomplishments'], work_history=user['work_history'],
                               professional_affiliation=user['professional_affiliation'],
                               computer_skills=user['computer_skills'])

    else:
        print("something is wrong")
        return '<p style="color: red;margin: 96px;">Something went wrong. ' \
               'Make sure you are submitting a pdf file!</p>'
def upload():
        if request.method == 'POST':
            uploaded_file = request.files['filename']
            file = secure_filename(uploaded_file.filename)  
            if file != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                        flash('wrong')
                        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
    
        return render_template('upload.html')

@app.route('/submit.html', methods=['POST'])
def submit():
    return render_template("submit.html")


if __name__ == '__main__':
    app.run()
