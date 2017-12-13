from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json
import subprocess

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None
default_rows = "15"
default_cols = "60"

default_Code = """#include <iostream>
using namespace std;
int main()
{

	return 0;
}
"""

if 'VCAP_SERVICES' in os.environ:
	vcap = json.loads(os.getenv('VCAP_SERVICES'))
	print('Found VCAP_SERVICES')
	if 'cloudantNoSQLDB' in vcap:
		creds = vcap['cloudantNoSQLDB'][0]['credentials']
		user = creds['username']
		password = creds['password']
		url = 'https://' + creds['host']
		client = Cloudant(user, password, url=url, connect=True)
		db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
	with open('vcap-local.json') as f:
		vcap = json.load(f)
		print('Found local VCAP_SERVICES')
		creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
		user = creds['username']
		password = creds['password']
		url = 'https://' + creds['host']
		client = Cloudant(user, password, url=url, connect=True)
		db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
	return render_template('home.html')

@atexit.register
def shutdown():
	if client:
		client.disconnect()

@app.route('/level', methods=['POST', 'GET'])
def test():
	code = default_Code
	resrun = 'Not running'
	rescompil = ''
	stin = ''
	if(request.method == "POST"):
		code = request.form["code"]
		(rescompil,resrun) = compileAndRunInput(code,stin)
	return render_template("looplevel.html",
						   levelnum=1,
						   code=code,
						   target="test",
						   resrun=resrun,
						   rescomp=rescompil,
						   rows=default_rows, cols=default_cols,
						   exoutput='',
						   stin='')


def compileAndRunInput(code,stin):
	x = ''
	y = 'Not Executed'
	goForRun = False
	f = open("a.cpp","w")
	f.write(code)
	f.close()
	try:
		x = subprocess.check_output(["g++","-Wall","a.cpp"],stderr=subprocess.STDOUT,timeout=1).decode()
		goForRun = True
	except Exception as e:
		x = e.output.decode()
	if(goForRun):
		x = x + "\n\nCompiled Sucessfully."
		try:
			l = subprocess.Popen(('echo', stin), stdout=subprocess.PIPE)
			y = subprocess.check_output(["./a.out"],stderr=subprocess.STDOUT,stdin=l.stdout,timeout=1).decode()
		except subprocess.TimeoutExpired as e:
			y = "Time Limit Exceeded."
		except Exception as e:
			y = e.output.decode()
	return (x,y)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
