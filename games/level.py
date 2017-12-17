from random import randint
import copy
import subprocess

levelDict = { "loops": [], "operators":[]}

class level:
	def __init__(self):
		self.solution= ''
		self.exout = ''
		self.input = ''
		self.lnum = 0
		self.comment = ''
		self.func = None

	def __str__(self):
		return self.solution + " " + self.exout+ " " + self.input + " " + self.lnum + " " + self.comment

def getLevel(s,n):
	n = int(n)
	if( s == "loops"):
		if(n< len(levelDict[s])):
			return levelDict[s][n]
	elif( s== "operators"):
		if(n < len(levelDict[s])):
			l = copy.copy(levelDict[s][n])
			x = randint(0,100)
			y = randint(0,100)
			z = l.func(x,y)
			l.input = str(x)+" "+str(y)
			l.exout = str(z)
			return l
	l = None
	return l

def checkOutput(code,lvl):
	if lvl.func != None :
		x = randint(0,100)
		y = randint(0,100)
		z = lvl.func(x,y)
		lvl.exout = z
		lvl.input = str(x) + " " + str(y)
	(rescompil,res) = compileAndRunInput(code,lvl)
	if res.rstrip()==str(lvl.exout).rstrip():
		return (rescompil,res,True)
	else:
		return (rescompil,res,False)

def compileAndRunInput(code,lvl):
	x = ''
	y = 'Not Executed'
	stin = lvl.input
	goForRun = False
	f = open("a.cpp","w")
	f.write(code)
	f.close()
	try:
		x = subprocess.check_output(["g++","-Wall","a.cpp"],stderr=subprocess.STDOUT,timeout=1).decode()
		goForRun = True
	except subprocess.TimeoutExpired as e:
		x = str(e)
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
	z = False
	return (x,y)

ques = level()
ques.comment = """ Try Simple Addition """
ques.func = lambda x,y : x + y
levelDict["operators"].append(ques)

ques = level()
ques.comment = """ Try Simple Multiplication """
ques.func = lambda x,y : x * y
levelDict["operators"].append(ques)

ques = level()
ques.comment = """ Do you notice perfect squares ? """
ques.func = lambda x,y : (x + y)*(x+y)
levelDict["operators"].append(ques)

ques = level()
ques.comment = """ It is a twisted addition :P """
ques.func = lambda x,y : x + 2 * y
levelDict["operators"].append(ques)

ques = level()
ques.comment = """ Combine your square logic with addition :D """
ques.func = lambda x,y : x * x + y
levelDict["operators"].append(ques)

ques = level()
ques.comment = """ No tricks here ! """
ques.input = '5'
ques.exout="""* 
* * 
* * * 
* * * * 
* * * * * """
levelDict["loops"].append(ques)

ques = level()
ques.comment = """ Just add spaces on both sides ! """
ques.input = '5'
ques.exout=""" * 
 *  * 
 *  *  * 
 *  *  *  * 
 *  *  *  *  * """
levelDict["loops"].append(ques)

ques = level()
ques.comment = """ Add another loop to print spaces equal to the number of row, before printing the character. Don't forget to make single spaced again ! """
ques.input = '5'
ques.exout=""" * 
  * * 
   * * * 
    * * * * 
     * * * * * """
levelDict["loops"].append(ques)

ques = level()
ques.comment = """ Add another loop to print spaces before printing the character. Don't forget to make single spaced again ! """
ques.input = '5'
ques.exout="""     * 
    * * 
   * * * 
  * * * * 
 * * * * * """
levelDict["loops"].append(ques)

ques = level()
ques.comment = """ Use Past Level's loop knowlege. Make a second loop and invert the outermost loop of the second set. """
ques.input = '5'
ques.exout=""" * 
  * * 
   * * * 
    * * * * 
     * * * * * 
     * * * * * 
    * * * * 
   * * * 
  * * 
 * """
levelDict["loops"].append(ques)

ques = level()
ques.comment = """ You know what to do here ;)  """
ques.input = '5'
ques.exout="""     * 
    * * 
   * * * 
  * * * * 
 * * * * * 
 * * * * * 
  * * * * 
   * * * 
    * * 
     * """
levelDict["loops"].append(ques)