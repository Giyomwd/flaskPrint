from flask import Flask,request,redirect,render_template
from powershell import PowerShell
import os

app = Flask(__name__)

def get_printerList():
   with open('templates/test.txt', 'r', encoding='utf-16') as printersInfo:
      printers =  printersInfo.read().split('|')
      list = []
      for i  in range(0,len(printers) -1):
         list.append(eval(printers[i]))
   return list
@app.route('/')
def init_printerList():
   return render_template('index.html', printerList=get_printerList())

@app.route('/updatePrinter/',methods=['POST'])
def updatePrinter():
   params = request.args if request.method == 'GET' else request.form
   printerName = params.get('printerName')
   portName = params.get('portName')
   print(printerName,portName)
   with PowerShell('GBK') as ps:
      outs, errs = ps.run('ping 127.0.0.1')
   print('error:', os.linesep, errs)
   print('output:', os.linesep, outs)
   return redirect('/')
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)