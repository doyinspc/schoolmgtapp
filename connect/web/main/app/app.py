from flask import Flask, render_template, make_response
import pdfkit

app = Flask(__name__)
@app.route('/')

def index():
    rendered = render_template('index.html', name='username')
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)