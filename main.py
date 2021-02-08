from flask import Flask, url_for, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import jinja2
import ast 
import os
from werkzeug.utils import secure_filename
from scanning import scan

env = jinja2.Environment()


app = Flask(__name__, template_folder='template')
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cvranking'
app.config['UPLOAD_FOLDER'] = './resumes'


mysql = MySQL(app)
app.jinja_env.globals.update(zip=zip, enumerate=enumerate)

#globals
job_id = 0
quiz_check = False
flag2 = 0
temp_id = 1

@app.route('/', methods=['GET', 'POST'])
def index():
	# session.pop('loggedin', None)
	# session.pop('id', None)
	# session.pop('username', None)
	# session.pop('_flashes', None)
	session.clear()
	if request.method == 'POST' and 'username' and 'pass' in request.form:
		# Create variables for easy access
		username = request.form['username'].lower()
		password = request.form['pass']
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (username, password,))
		# Fetch one record and return result
		account = cursor.fetchone()
		if account:
			# Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['id'] = account['id']
			session['useremail'] = account['email']
			# Redirect to home page
			return redirect(url_for('view_job'))
		else:
			# Account doesnt exist or username/password incorrect
			flash('Please enter correct username and password', 'error')
			return render_template('index.html')
	return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	session.clear()
	if request.method == 'POST' and 'username' and 'pass' in request.form:
		# Create variables for easy access
		username = request.form['username'].lower()
		password = request.form['pass']
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin_accounts WHERE email = %s AND password = %s', (username, password,))
		# Fetch one record and return result
		account = cursor.fetchone()
		if account:
			# Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			# Redirect to home page
			return redirect(url_for('view_jobs'))
		else:
			# Account doesnt exist or username/password incorrect
			flash('Please enter correct username and password', 'error')

	return render_template('admin_login.html')

@app.route("/view_jobs", methods=['GET', 'POST'])
def view_job():
	global quiz_check
	quiz_check =True
	if session.get('loggedin'):
		# fetching jobs data from database
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT job_id FROM job_details')
		job_id = cursor.fetchall()

		cursor.execute('SELECT job_title FROM job_details')
		job_title = cursor.fetchall()

		cursor.execute('SELECT location FROM job_details')
		location = cursor.fetchall()

		cursor.execute('SELECT min_salary FROM job_details')
		min_salary = cursor.fetchall()
		if min_salary:
			min_salary[0]['min_salary'] = format_salary(min_salary[0]['min_salary'])

		cursor.execute('SELECT max_salary FROM job_details')
		max_salary = cursor.fetchall()
		if max_salary:
			max_salary[0]['max_salary'] = format_salary(max_salary[0]['max_salary'])

		cursor.execute('SELECT company_name FROM job_details')
		company_name = cursor.fetchall()

		cursor.execute('SELECT job_description FROM job_details')
		job_description = cursor.fetchall()

		cursor.execute('SELECT skills FROM job_details')
		skills = cursor.fetchall()
		#==============================================================
		if job_title:
			return render_template('view_jobs.html',quiz_no=1, job_id=job_id, job_title=job_title, location=location, min_salary=min_salary, max_salary=max_salary, company_name=company_name, job_description=job_description, skills=skills)
		else:
			return render_template('view_jobs.html')
	return redirect(url_for('index'))

@app.route("/jobs", methods=['GET', 'POST'])
def view_jobs():
	if session.get('loggedin'):
		# fetching jobs data from database
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT job_id FROM job_details')
		job_id = cursor.fetchall()

		cursor.execute('SELECT job_title FROM job_details')
		job_title = cursor.fetchall()

		cursor.execute('SELECT location FROM job_details')
		location = cursor.fetchall()

		cursor.execute('SELECT min_salary FROM job_details')
		min_salary = cursor.fetchall()
		if min_salary:
			min_salary[0]['min_salary'] = format_salary(min_salary[0]['min_salary'])

		cursor.execute('SELECT max_salary FROM job_details')
		max_salary = cursor.fetchall()
		if max_salary:
			max_salary[0]['max_salary'] = format_salary(max_salary[0]['max_salary'])

		cursor.execute('SELECT company_name FROM job_details')
		company_name = cursor.fetchall()

		cursor.execute('SELECT job_description FROM job_details')
		job_description = cursor.fetchall()

		cursor.execute('SELECT skills FROM job_details')
		skills = cursor.fetchall()
		#==============================================================
		if job_title:
			return render_template('admin_portal.html', job_id=job_id, job_title=job_title, location=location, min_salary=min_salary, max_salary=max_salary, company_name=company_name, job_description=job_description, skills=skills)
		else:
			return render_template('admin_portal.html')
	return redirect(url_for('index'))

@app.route("/add_jobs", methods=['GET', 'POST'])
def add_job():
	if session.get('loggedin'):
		if (request.method == 'POST') and ('job_title' and 'company_name' and 'com_location' and 'experience' and 'min_salary' and 'max_salary' and 'skills' and 'job_description' in request.form):
			job_title = request.form['job_title'].lower()
			company_name = request.form['company_name'].lower()
			com_location = request.form['com_location'].lower()
			experience = request.form['experience']
			min_salary = request.form['min_salary']
			max_salary = request.form['max_salary']
			skills = request.form['skills'].lower()
			job_description = request.form['job_description'].lower()

			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO job_details VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (job_title, company_name, com_location, experience, min_salary, max_salary, skills, job_description,))
			mysql.connection.commit()
			return redirect(url_for('view_jobs'))
		return render_template('add_jobs.html')
	return redirect(url_for('index'))

@app.route('/update_job', methods=['GET', 'POST'])
def update_job():
	global job_id
	if session.get('loggedin'):
		# print(session['loggedin'])
		if request.method == 'POST':
			if request.form.get('search') and 'job_id' in request.form:
				job_id = request.form['job_id']
				print('yes')
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM job_details WHERE job_id = %s', (job_id,))
				data = cursor.fetchall()
				
				if data:
					return render_template("update_jobs.html", data=data)
					
				else:
					flash("Job Id is invalid!", 'error')
					return render_template("update_jobs.html")
			
			if (request.form.get('submit')) and ('job_title' and 'company_name' and 'com_location' and 'experience' and 'min_salary' and 'max_salary' and 'skills' and 'job_description' in request.form) and (int(job_id) > 0):
				print("update")
				job_title = request.form['job_title'].lower()
				company_name = request.form['company_name'].lower()
				com_location = request.form['com_location'].lower()
				experience = request.form['experience']
				min_salary = request.form['min_salary']
				max_salary = request.form['max_salary']	
				skills = request.form['skills'].lower()
				job_description = request.form['job_description'].lower()

				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute("UPDATE job_details SET job_title = %s, company_name = %s, location = %s, exp_required = %s, min_salary = %s, max_salary = %s, skills = %s, job_description = %s WHERE job_id = %s", (job_title, company_name, com_location, experience, min_salary, max_salary, skills, job_description, job_id,))
				mysql.connection.commit()	

				return redirect(url_for('view_jobs'))
			
			elif request.form.get('delete') and (int(job_id) > 0):
				print("Delete")
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute("DELETE FROM job_details WHERE job_id = %s", (job_id,))
				mysql.connection.commit()

				return redirect(url_for('view_jobs'))
			
			else:
				flash("Job ID is missing try again!")
				return render_template("update_jobs.html")

		else:
			return render_template("update_jobs.html")
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def registration():
	session.clear()
	if request.method == 'POST'and 'username' and 'pass' and 'useremail' and 'phno' and 'confirm_pass' in request.form:
		# Create variables for easy access
		username = request.form['username'].lower()
		useremail = request.form['useremail'].lower()
		phno = request.form['phno']
		password = request.form['pass']
		conf_password = request.form['confirm_pass']

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = %s', (useremail,))
		account = cursor.fetchone()
		if account:
			flash('Account already exists!')
		
		elif password == conf_password:

			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username, useremail, phno, password,))
			mysql.connection.commit()
			return redirect(url_for('index'))
		else:
			flash("Confirm password is not same as password!")
		
	return render_template('registration.html')

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
	global job_id
	ran = True
	if session.get('loggedin'):
		# print(session['loggedin'])
		if request.method == 'POST':
			if request.form.get('search'):
				job_id = request.form['job_id']
				print('yes')
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM job_details WHERE job_id = %s', (job_id,))
				data = cursor.fetchall()
				
				if data:
					flash("Authentication Succefull! Please add quiz below")
					return render_template("add_quiz.html", ran=ran)
					
				else:
					flash("Job Id is invalid!", 'error')
					return render_template("add_quiz.html", ran=ran)
			if request.form.get('add') and ('quiz_no' and 'question' in request.form) and (int(job_id) > 0):
				print("add_quiz")
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				questions= []
				quiz_no = request.form.get('quiz_no')
				question = request.form['question']
				question_1 = request.form['question_1']
				question_2 = request.form['question_2']
				question_3 = request.form['question_3']
				question_4 = request.form['question_4']
				question_ans = request.form['question_ans']

				temp_no = int(quiz_no)
				quiz_c = 0
				quiz_flag = False
				while temp_no>1:
					temp_no -= 1
					cursor.execute('SELECT * FROM quizzes WHERE job_id=%s AND quiz_no=%s', (job_id, str(temp_no)))
					temp_data2 = cursor.fetchone()
					if temp_data2:
						continue
					else:
						quiz_flag = True
						quiz_c += 1
				if quiz_flag:
					print(quiz_c)
					flash("Please select quiz number as {}".format(int(quiz_no) - quiz_c))
					return render_template("add_quiz.html", ran=ran)

				questions.append(job_id)
				questions.append(quiz_no)
				temp_q = {}
				temp_q['{}'.format(question)] = ['{}'.format(question_1), '{}'.format(question_2), '{}'.format(question_3), '{}'.format(question_4), '{}'.format(question_ans)]

				questions.append("{}".format(temp_q))

				cursor.execute('SELECT * FROM quizzes WHERE job_id=%s AND quiz_no=%s', (job_id, quiz_no))
				temp_data = cursor.fetchall()
				print(temp_data)

				if temp_data:
					q = ast.literal_eval(temp_data[0]['questions'])
					q['{}'.format(question)] = ['{}'.format(question_1), '{}'.format(question_2), '{}'.format(question_3), '{}'.format(question_4), '{}'.format(question_ans)]
					
					cursor.execute('UPDATE quizzes SET questions=%s WHERE job_id=%s AND quiz_no=%s', ("{}".format(q), job_id, quiz_no))
					mysql.connection.commit()
				
				else:
					holder ="INSERT INTO quizzes VALUES (NULL, %s)" %", ".join("%s" for _ in questions)
					cursor.execute(holder, (questions))
					mysql.connection.commit()

				flash("Quiz Successfully Added!")
				return render_template("add_quiz.html")
			else:
				flash("Quiz Not Added!")
				render_template("add_quiz.html", ran=ran)
		else:
			render_template("add_quiz.html")
	return render_template("add_quiz.html")

@app.route('/quiz_portal', methods=['GET', 'POST'])
def quiz_portal():
	global job_id
	if session.get('loggedin'):
		if request.method == 'POST':
			if request.form.get('search') and 'job_id' in request.form:
				job_id = request.form['job_id']
				print('yes')
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM job_details WHERE job_id = %s', (job_id,))
				data = cursor.fetchall()
				
				if data:
					flash("Authentication Succefull!")
					if int(job_id) > 0:
						cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
						cursor.execute('SELECT * FROM quizzes WHERE job_id = %s', (job_id,))
						data = cursor.fetchall()
						# print(data)
						res = []
						for i in data:
							res.append(get_quiz_title(i))
					return render_template("quiz_portal.html", ran=True, data=res)
					
				else: 	
					flash("Job Id is invalid!", 'error')
					return render_template("quiz_portal.html", ran=False)
		else:
			return render_template("quiz_portal.html", ran=False)
	return redirect(url_for('index'))

@app.route('/<quiz_no>kkkk<job_id>', methods=['GET', 'POST'])
def quiz(quiz_no, job_id):
	global quiz_check, flag2, temp_id
	if session.get('loggedin'):
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		quiz_no = int(quiz_no)
		track_quiz = quiz_no
		flag = False
		while track_quiz<=5:
			print("job_id: " + str(job_id) + " quiz: " + str(quiz_no))
			cursor.execute('SELECT * FROM quizzes WHERE job_id = %s AND quiz_no=%s', (job_id, quiz_no,))
			data = cursor.fetchall()
			print(data)
			questions = []
			answers = []
			if data:
				if flag2 < 1:
					temp_id = data[0]['id']
					flag2 = 1
				quiz_id = temp_id
				temp_q = data[0]['questions']
				temp_q = ast.literal_eval("%s"%(temp_q))
				for i in temp_q:
					temp_q[i] = ast.literal_eval("%s"%(temp_q[i]))
					questions.append({i: temp_q[i]})
					answers.append(temp_q[i][4])
				print("questions: "+str(questions))
				break
			else:
				quiz_no += 1
				track_quiz += 1
				flag = True
		if flag:
			quiz_no = 6

		if request.method == 'POST':

			user_answers = []
			for i in range(1,100):
				try:
					user_answers.append(str(request.form['ques_{}'.format(i)]))
				except KeyError:
					break
			score = 0
			for a, b in zip(answers, user_answers):
				# print("a: {}, b: {}".format(a,b))
				if a == b:
					score +=1
			score = (score/len(answers))*100
			print("Your score: "+str(score) + 'id: '+str(session['id']))
			cursor.execute('SELECT * FROM result WHERE account_id=%s AND quiz_id = %s', (session['id'], quiz_id))
			data = cursor.fetchall()

			cursor.execute('SELECT * FROM result WHERE account_id=%s', (session['id'],))
			data2 = cursor.fetchone()
			print(data2)

			if data:
				print('****************')
				print(quiz_check)
				if quiz_check != True:
					score = str(data[0]['score'])+ ", " + str(score)
				cursor.execute('UPDATE result SET score=%s WHERE (account_id=%s AND quiz_id=%s)', (score, session['id'], quiz_id))
				mysql.connection.commit()
				quiz_check = False
			elif data2:
				cursor.execute('UPDATE result SET score=%s, quiz_id=%s WHERE (account_id=%s)', (score, quiz_id, session['id']))
				mysql.connection.commit()
			else:
				cursor.execute('INSERT INTO result (account_id, quiz_id, score) VALUES (%s, %s, %s)', (session['id'], quiz_id, score))
				mysql.connection.commit()
			quiz_no +=1
			while track_quiz<=5:
				print("job_id: " + str(job_id) + " quiz: " + str(quiz_no))
				cursor.execute('SELECT * FROM quizzes WHERE job_id = %s AND quiz_no=%s', (job_id, quiz_no,))
				data = cursor.fetchall()
				print(data)
				questions = []
				answers = []
				if data:
					quiz_id = data[0]['id']
					temp_q = data[0]['questions']
					temp_q = ast.literal_eval("%s"%(temp_q))
					for i in temp_q:
						temp_q[i] = ast.literal_eval("%s"%(temp_q[i]))
						questions.append({i: temp_q[i]})
						answers.append(temp_q[i][4])
					print("questions: "+str(questions))
					break
				else:
					quiz_no += 1
					track_quiz += 1
					flag = True
			if quiz_no < 5:
				return redirect(url_for("quiz", quiz_no=quiz_no, job_id=job_id))
			else:
				return redirect(url_for('resume'))
		else: 
			return render_template('quiz.html', questions=questions, quiz_no=quiz_no, job_id=job_id)
	else:
		return redirect(url_for("index")) 

@app.route('/remove_quiz', methods=['GET', 'POST'])
def update_quiz():
	if session.get('loggedin'):
		res = []
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM quizzes')
		data = cursor.fetchall()
		if data:
			for i in data:
				res.append(get_quiz_title(i))
		if request.method == 'POST':
			if request.form.get('remove') and "quiz_id" in request.form:
				quiz_id = request.form['quiz_id']

				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute("DELETE FROM quizzes WHERE ID = %s", (quiz_id,))
				mysql.connection.commit()
				flash("Quiz Removed")
				return redirect(url_for('update_quiz'))	
			else:
				flash("Quiz ID is invalid!")
				return render_template('remove_quiz.html')
		else:
			if res:
				return render_template('remove_quiz.html', data=res)
			else:
				flash('NO QUIZ FOUND!')
				return render_template('remove_quiz.html', data=res)

	else:
		return redirect(url_for("index"))

@app.route('/resume', methods=['GET', 'POST'])
def resume():
	if session.get('loggedin'):
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT cv_name FROM result WHERE account_id = %s', (session['id'],))
		data = cursor.fetchall()
		res = []
		if data:
			print(data)
			for x in data:
				res.append(x['cv_name'])
			# res.pop()
		if request.method == 'POST':
			file_ = request.files['filename']
			print('this is filename: ')
			print(file_)
			filename = make_unique(file_.filename)
			if filename != '':
				filename = filename.replace(" ", '-')
				file_.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(filename)))
				cursor.execute('SELECT * FROM result WHERE account_id = %s', (session['id'],))
				data_ = cursor.fetchall()
				if data_:
					cursor.execute('UPDATE result SET cv_name=%s WHERE account_id=%s', (filename, session['id']))
					mysql.connection.commit()
				else:
					cursor.execute('INSERT INTO result (account_id, cv_name) VALUES (%s, %s)', (session['id'], filename))
					mysql.connection.commit()
			flash("Resume Uploaded!")
		return render_template('upload_resume.html', res=res)
	else:
		return redirect(url_for('index'))

@app.route('/result', methods=['GET', 'POST'])
def result():
	global job_id
	if session.get('loggedin'):
		if request.form.get('search') and 'job_id' in request.form:
				job_id = request.form['job_id']
				print('yes')
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM job_details WHERE job_id = %s', (job_id,))
				data = cursor.fetchall()
				print(data)
				try:
					f = open('./temp_resume/job_{}.txt'.format(job_id), 'w')
					f.write(str(data[0]['skills'])+ str(data[0]['job_description']))
					f.close()
				except Exception as e:
					print(e)
				if data:
					job = 'job_{}.txt'.format(job_id)
					res = scan(job)
					cursor.execute('SELECT * FROM result')
					data = cursor.fetchall()
					print(res)
					scores_dict = {}
					acc = {}
					if data:
						for i in data:	
							print("yes: "+i['cv_name'])
							if i['cv_name'] in res:
								temp = list(i['score'].split(','))
								temp = list(map(lambda x: x.replace(" ", ""), temp))
								temp = list(map(float, temp))
								print("temp: "+ str(temp))
								isfail = True
								for j in temp:
									if j < 75:
										res.pop(i['cv_name'])
										isfail = False
										break
								acc[i['cv_name']] = i['account_id']
								if isfail:
									scores_dict[i['cv_name']] = i['score']
						
						for i in res:
							if i in scores_dict:
								continue
							else:
								res.pop(i)
							
						scores = []
						print("Dict: "+str(scores_dict))
						count = 0
						for i in scores_dict:
							if count < 10:
								if acc:
									print("name: "+i)
									cursor.execute('INSERT INTO user_result VALUES (NULL, %s, %s)', (acc[i], "You are shortlisted for job id: {}".format(job_id)))
									mysql.connection.commit()
									count +=1 

						for i in res:
							scores.append(scores_dict[i])
						print(scores)
					
					os.remove('./temp_resume/job_{}.txt'.format(job_id))
					flash("Scanning Successful! Scroll down to see result")
					return render_template("result.html", res=res, scores=scores)
					
				else:
					flash("Job Id is invalid!", 'error')
					return render_template("result.html")
		return render_template("result.html")
	return redirect(url_for('index'))

@app.route('/user_result', methods=['GET', 'POST'])
def user_result():
	if session.get('loggedin'):
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT message FROM user_result WHERE account_id=%s", (session['id'],))
		data = cursor.fetchone()
		if data:
			return render_template('user_result.html', mes=data['message'])
		else:
			return render_template('user_result.html')
	else:
		return redirect(url_for('index'))

from uuid import uuid4
def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"	

def format_salary(sal):
	sal = str(sal)
	if len(sal) >=3:
		sal = sal[:-3]
	return int(sal)

def get_quiz_title(datastr):
	print(datastr)
	# print(type(ast.literal_eval(datastr['question_1'])["1) What is the maximum possible length of an identifier?"]))
	return (datastr['quiz_no'], datastr['id'], datastr['job_id'])

if __name__ == '__main__':
	app.run(debug=True)