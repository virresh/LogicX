from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, escape
import atexit
import cf_deployment_tracker
import os
import json
import games.level

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)
app.secret_key = 'YouThinkYouCanGetThisSoEasilyThenYouAreWrong'

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
	if 'secretkey' in vcap:
		app.secretkey = vcap['secretkey']
elif os.path.isfile('vcap-local.json'):
	with open('vcap-local.json') as f:
		vcap = json.load(f)
		print('Found local VCAP_SERVICES')
		app.secret_key = vcap['secretkey']

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/',methods=['POST', 'GET'])
def home():
	if('username' in session):
		return render_template('home.html', name=session['username'], track=session.get('track'), level=session.get(session.get('track')),loopL=session.get('loops'),opL=session.get('operators'))
	else:
		if (request.form.get('name')!=None and request.method=="POST"):
			session['username'] = request.form['name']
			session['track'] = None
			session['level'] = None
			session['operators'] = '0'
			session['loops'] = '0'
			return home()
		return render_template('login.html')

@app.route('/level', methods=['POST', 'GET'])
def test():
	
	resrun = 'Not running'
	rescompil = ''
	stin = ''
	exout = ''
	success = session.get('success')
	session['success'] = None

	if(request.method =="POST"):
		y = request.form.get('track')
		z = request.form.get('level')
		if(y == None or z == None ):
			return redirect(url_for('home'))
		session['track'] = y
		session['level'] = z
		session[session['track']] = z

	lv = games.level.getLevel(session.get('track'),session.get('level'))
	if(lv==None):
		return redirect(url_for('home'))
	stin = lv.input
	exout = lv.exout
	
	if(session.get('track') == "loops"):
		default_Code = '''#include <iostream>
using namespace std;
int main()
{
    int n;
    cin>>n;
    for(int i=1; i<=n; i++){
        for(int j=1; j<=i; j++){
            cout<<"* ";
        }
        cout<<"\\n";
    }
	return 0;
}'''
	elif (session.get('track') == "operators"):
		default_Code = '''#include <iostream>
using namespace std;
int main()
{
    int a,b;
    cin>>a>>b;
    cout<<a+b<<"\\n";
	return 0;
}'''
	
	code = default_Code
	
	if(request.method == "POST"):
		code = request.form.get("code")
		if code != None:
			(rescompil,resrun,success) = games.level.checkOutput(code,lv)
			stin = lv.input
			exout = lv.exout
			if(success):
				session['level'] = str(int(session['level']) + 1)
				session[session['track']] = session['level']
				session['success'] = True;
				return redirect(url_for('test'))
			else:
				session['success'] = None
		else:
			code = default_Code
	return render_template("looplevel.html",
						   levelnum=session.get(session.get('track')),
						   code=code,
						   target="test",
						   resrun=resrun,
						   rescomp=rescompil,
						   rows=default_rows, cols=default_cols,
						   exoutput=exout,
						   stin=stin,
						   track=session['track'],
						   success=success,
						   hint=lv.comment)

@app.route('/reset')
def reset():
	session.pop('username',None)
	session.pop('track',None)
	session.pop('level',None)
	return home()


# @atexit.register
# def shutdown():
# 	#Currently empty function, should change hopefully soon
# 	pass

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
