from flask import Flask, render_template, request, flash
from flask_bootstrap5 import Bootstrap
import PyPDF2

UPLOAD_FOLDER = '/static/resume_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)

user = {}


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/upload.html')
def upload():
    return render_template("upload.html")


@app.route('/display.html', methods=['POST'])
def display():
    if request.method == 'POST' and 'filename' in request.files \
            and request.files['filename'].content_type == 'application/pdf':

        file = request.files['filename']
        pdfReader = PyPDF2.PdfFileReader(file)

        # Getting number of pages in pdf file
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
            user['name'] = text[5] + text[6] + text[7] + text[8]
            print("name = " + user['name'])
            user['email'] = text[18]
            print("email = " + user['email'])

            for j in range(len(text)):
                # Printing the line
                # Lines are separated using "\n"
                print(text[j], end="\n")
                # For Separating the Pages

        # process more info about file
        print("file sent successfully")
    else:
        print("something is wrong")
        return '<br><p style="color: red">Make sure you are submitting a pdf file!</p>'
    return render_template("display.html")


if __name__ == '__main__':
    app.run()
