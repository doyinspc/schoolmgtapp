from flask import Flask, render_template, make_response, send_file
from flask_bootstrap import Bootstrap
from connect import Db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import pdfkit
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.backend_bases.FigureCanvas import FigureCanvas
import StringIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def index2():
    return render_template('bodybar.html')
    

@app.route('/<session>/<student>/<subject>/<ca>')
def index(session, student, subject, ca):
    #_session = session
    #_student = student.split(',')
    #_subject = subject.split(',')
    #_ca = ca.split(',')

    _session = '8'
    session = '8'
    _student = [u'487', u'488', u'489', u'490', u'491', u'492', u'493', u'494', u'495', u'496', u'497', u'498', u'499', u'501', u'502', u'504', u'505', u'506', u'507', u'508']
    _subject = [u'32', u'33', u'34', u'35', u'36', u'37']
    ca = "46,47,48"
    _ca = ca.split(',')
    
    _subject_arr = getSubName(_subject)
    _ca_arr = getSub(_ca)
    _student_arr = getName(1, _student)
    _student_arrs = getName(0, _student)
    cols = len(_ca) + 1
    f = data(_session, _student, _subject, _ca)
    y = struc(f[1], _student, _subject, _ca)
    comp = comput(y[0], _student_arrs)
    comp1 = comput1(y[0], _subject_arr)
    
    fig = plot_signal()
    #fig = convert_fig_to_html(ppl)
    return render_template('index.html', immg =fig,  name=y, cols=cols,  session=session, subject=_subject_arr, student=_student_arr, ca = _ca_arr, data=f[0], table=comp , table1=comp1 )
    #path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    #config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    #pdf = pdfkit.from_url(rendered, output_path = 'MyPDF.pdf', configuration=config)
    ##pdf = pdfkit.from_url(url=rendered, output_path=False, configuration=config)
    #pdf = pdfkit.from_string(body, 'outtry.pdf', configuration=config) #with --page-size=Legal and --orientation=Landscape
    #pdf = pdfkit.from_string(rendered, 'try.pdf')
    #pdfkit.setOptions(['ignoreWarnings'=>true])
    #response = make_response(pdf)
    #response.headers['Content-Type'] = 'application/pdf'
    #response.headers['Content-Disposition'] = 'inline;outpu.pdf'
    #return response

def plot_signal(a={}):
    # Skipping a lot of other complexity her
    #ax = plt.subplots(figsize=(300, 400))
    figure = plt.figure()
    plt.figure(1)
    plt.subplot(111)
    plt.plot([1,2,3,4], [6,7,8,9])
    data = plt.savefig('temp.png')
    
  
    return '<img src="data:image/png;base64,{}">'
    # further stuff
    #return plt


def convert_fig_to_html(fig):
  """ Convert Matplotlib figure 'fig' into a <img> tag for HTML use using base64 encoding. """
  canvas = FigureCanvas(fig)
  png_output = StringIO.StringIO()
  canvas.print_png(fig)
  data = png_output.getvalue().encode('base64')
  
  return '<img src="data:image/png;base64,{}">'.format(urllib.quote(data.rstrip('\n')))

def data(session, student, subject, ca):
    rtt1 = getStudentAssessments(session, student, subject, ca)
    _arr={}
    for g in rtt1:
        st = 'AB'+str(g['studentID'])+'CD'+str(g['subjectID'])+'EF'+str(g['caID'])
        _arr.update({st: g['score'] * float(g['mmax'])})
    return [_arr, rtt1]

def struc(data, student, subject, ca):
    _arr={}
    for g in data:
        st = 'AA'+str(g['studentID'])+'BB'+str(g['subjectID'])
        if st in _arr:
            pass
        else:
            _arr.update({st : []})
        tot =   g['score'] * float(g['mmax']) 
        _arr[st].append(tot)
        
    n_arr ={} 
    m_arr ={}
    for s in student:
        n_arr.update({s:{}})
        m_arr.update({s:{}})
        for su in subject:
           st = 'AA'+str(s)+'BB'+str(su)
           if st in _arr:
               k = sum(_arr[st])  
               y = len(_arr[st])
           else:
               k = 0
               y = 0
            
           n_arr[s].update({su:k})
           m_arr[s].update({su:y})
           
    return [n_arr, m_arr]      
               
 
def comput(data={}, students={}):
    df = pd.DataFrame(data)
    df.rename(columns=students, inplace=True)
    d4 = df.sum()
    d6 = d4.rank(method='min', ascending=False)
    d2 =df.describe()
    d3 = d2.transpose()
    d5 = pd.concat([d3, d4] ,axis=1, sort=True)
    d5.rename(columns={0:'SUM'}, inplace=True)
    d7 = pd.concat([d5, d6] ,axis=1, sort=True)
    d7.rename(columns={0:'RANK'}, inplace=True)
    d8 = d7.round(1)
    d8['count'] = d8['count'].apply(np.round)
    descc = 0
    d8['RANK'] = d8['RANK'].apply(lambda x: round(x, descc))
    return d8.to_html()
 
def comput1(data={}, subject={}):
    df = pd.DataFrame(data)
    df1 = df.transpose()
    df1.rename(columns=subject, inplace=True)
    d2 = df1.describe()
    d3 = d2.transpose()
    #d3.index.rename('Subjects', inplace=True)
    return d3.to_html()
    
    
def getStudentAssessments(session, student=[], subject=[], ca=[]):
    _session = session
    _student = student
    _subject = subject
    _ca = ca
    g = Db()
    data = g.selectStudentsCaRep(_session, _student, _subject, _ca)
    return data

def getSub(b=[]):
    store_sub_name = {}
    cn = Db()
    for subz in b:
        sub_name = None
        sub_name = cn.selectn('datas','', 1, {'id':subz})
        if sub_name:
            store_sub_name.update({subz:sub_name['abbrv']}) 
       
    return store_sub_name

def getSubName(b=[]):
    store_sub_name = {}
    cn = Db()
    for subz in b:
        sub_name = None
        sub_name = cn.selectn('datas','', 1, {'id':subz})
        if sub_name:
            store_sub_name.update({subz:sub_name['name']}) 
       
    return store_sub_name

def getName(a, b=[]):
    store_sub_name = {}
    cn = Db()
    for subz in b:
        sub_name = None
        sub_name = cn.selectn('students','', 1, {'id':subz})
        if sub_name:
            if(a == 0):
                nam = str(sub_name['surname']+' '+sub_name['firstname']).title()
                store_sub_name.update({subz: nam }) 
            elif(a == 1):
                nm = str(sub_name['surname']+' '+sub_name['firstname']).title()
                nam = [sub_name['schno'], nm]
                store_sub_name.update({subz: nam }) 
    return store_sub_name



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)