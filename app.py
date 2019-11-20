from flask import Flask,request,redirect,render_template
from powershell import PowerShell
import  sqlserver_crud as db
app = Flask(__name__)

@app.route('/')
def init_printerList():
   return render_template('nologin_index.html', printerList=db.getPrinterLatestData())

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/updatePrinter/',methods=['POST'])
def updatePrinter():
   params = request.args if request.method == 'GET' else request.form
   newPrinterName = params.get('printerName')
   portName = params.get('portName')
   oldPrinterName = db.getOldPrinterName(portName,newPrinterName)
   db.updatePrinterInfo(newPrinterName,oldPrinterName,portName)

   with PowerShell('GBK') as ps:
      ps.run(r'.\Set-PrinterInfo.ps1 -Type {0} -PortName {1} -PrinterName {2} -OldPrinterName {3}'.format('UPDATE',portName,newPrinterName,oldPrinterName))
   return redirect('/')

@app.route('/deletePrinter/',methods=['POST'])
def deletePrinter():
   printerName =  request.values['printerName']
   db.deletePrinterByPrinterName(printerName)
   with PowerShell('GBK') as ps:
      ps.run(r'.\Set-PrinterInfo.ps1 -Type {0} -PrinterName {1}'.format('DELETE',printerName))
   return  'success'

@app.route('/addPrinter/',methods=['POST'])
def addPrinter():
   params = request.args if request.method == 'GET' else request.form
   printerName = params.get('printerName')
   portName = params.get('portName')
   db.addPrinter(printerName,portName)
   with PowerShell('GBK') as ps:
      ps.run(r'.\Set-PrinterInfo.ps1 -Type {0} -PortName {1} -PrinterName {2} -OldPrinterName {3}'.format('UPDATE',portName,printerName,printerName))
   return redirect('/')

@app.route('/updateCheckStatus/',methods=['POST'])
def updateCheckStatus():
   checkStatus = 'Y' if request.values['checkstatus'] == 'true' else 'N'
   printerName = request.values['printername']
   db.updatePrinterCheckStatus(printerName,checkStatus)
   return 'success'

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)