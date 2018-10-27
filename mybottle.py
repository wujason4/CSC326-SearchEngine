# from bottle import route, template, run, static_file
from bottle import *
import collections
import re
import httplib2
from beaker.middleware import SessionMiddleware
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
############
#  TO DO:  #
############
# - decide whether to store history as DEQUEUE or ORDEREDDICT
# - change all of the .format() to f-string

history = collections.OrderedDict()
HISTORY_MAX_LENGTH = 20
SCOPES = ['https://www.googleapis.com/auth/plus.me ','https://www.googleapis.com/auth/userinfo.email']

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True
}

app = SessionMiddleware(app(),session_opts)
user_searchHistory = {}

# Home Page
@route('/')
def home_page():
	print "WUTWUTUWUT"
	session = request.environ.get('beaker.session')
	
	user_email = session['user_email'] if 'user_email' in session else False
	user_name = session['user_name'] if 'user_name' in session else ''
	user_pic = session['user_pic'] if 'user_pic' in session else ''
	user_history = user_searchHistory[email] if email in history else {}
	
	print"====DEFAULT SESSION======"
	print session
	print"====DEFAULT SESSION======"

	pic = 'logo.png'
	return template('home_page', picture=pic)


# Static CSS file for the home_page table
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/login','GET')
def login():
	print "signing in"
	session = request.environ.get('beaker.session')
	flow = flow_from_clientsecrets("client_secrets.json",
						scope= SCOPES, 
						redirect_uri="http://localhost:8080/redirect",
						prompt="select_account")
	uri = flow.step1_get_authorize_url()
	return redirect(str(uri))
	
@route ('/logout')
def logout():
	session = request.environ.get('beaker.session')
	session.delete()
	print "=============================12==============================\n"
	print "sign out success"
	print "=============================12==============================\n"
	return redirect('/')

@route ('/redirect')
def redirect_page():
	code = request.query.get('code','')
	flow = OAuth2WebServerFlow(client_id = '80715897647-7q7d2n7ginn7arer5a5dh0gu254vqtuq.apps.googleusercontent.com',
								client_secret='uyIulo6GxU9sA8oLb4P365Vm',
								scope=SCOPES,
								redirect_uri="http://localhost:8080/redirect")

	credentials = flow.step2_exchange(code)
	token = credentials.id_token['sub']

	http = httplib2.Http()
	http = credentials.authorize(http)

	#Get user email
	users_service = build('oauth2','v2',http=http)
	user_document = users_service.userinfo().get().execute()
	print "=============================56==============================\n"
	print user_document
	print "=============================56==============================\n"
	
	session = request.environ.get('beaker.session')
	session['user_email'] = user_document['email']
	session['user_name'] = user_document['name']
	session['pic'] = user_document['picture']
	session.save()
	
	print "=============================67==============================\n"
	print session
	print "=============================67==============================\n"
	# After logging in go back to home page
	print "DONEDONEDONE"
	redirect('/')


@post('/search')
def show_results(stable='', htable=''):
		session = request.environ.get('beaker.session')
		user_email = session['user_email'] if 'user_email' in session else ''

		if user_email not in user_searchHistory:
			user_searchHistory[user_email] = set() 


		# Get the search string
		original_string = request.forms.get('keywords')
		
		# Initialize the dictionary of unique words
		keyword_set = dict()
		global history
		checked = []

		# Extract whole words from the search string, may include repeats
		# **Should return ['word1', 'word2', 'word3']
		# char_regex = r"[^\W\?$]|[^']|"
		# string = re.sub(char_regex, '', original_string)

		# print "\n\nafter char_regex: ", string
		string = original_string.split()
		# print "after split: ", string
		
		# Extract all unique words and store with count
		for word in string:

			regex = r"\b" + re.escape(word) + r"\b"
			count = sum(1 for match in re.finditer(regex, original_string))

			if word not in keyword_set:
						keyword_set[word] = count
					
		print "HISTORY_LENGTH: ", len(history)

		
		# For every unique searched word
		for s_word, s_count in keyword_set.items():

			# Check if word already in history
			if s_word in history:
				history[s_word] += s_count
			
			# word not in history, delete an entry from history and add new word
			else:

				# Check if history has reached max length
				if len(history) < HISTORY_MAX_LENGTH:
					history[s_word] = s_count

				else:
					min_searched_count = min(history.values())

					# Delete min searched word
					for h_word, h_count in history.items():

						if h_count == min_searched_count:
							del history[h_word]
							break

					# Add newly searched to history
					history[s_word] = s_count


		# Sort histrory in DESCENDING order
		sorted_history = collections.OrderedDict(sorted(history.iteritems(), key=lambda (k,v): (v,k), reverse=True))
		
		for word in sorted_history:
			print '==========89=========\n'
			print word
			print '==========89=========\n'
			user_searchHistory[user_email].add(word)

		for w in user_searchHistory[user_email]:
			print '==========90=========\n'
			print w
			print '==========90=========\n'
		##############################	
		# Create the table!! #
		##############################
		# 1) Style the table firsts
		final_table = "<table>"
		history_table = "<table>"
		
		# 2) Add the table heading
		final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>".format(original_string)
		history_table += "<thead><tr><th colspan=\"2\">Top 20 Searched</th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>"


		# 3) Add the table data
		for i in keyword_set:
			final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

		for key, value in sorted_history.iteritems():
			history_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)


		# 4) Close off the table
		final_table = final_table + "</tbody></table>"
		history_table = history_table + "</tbody></table>"


		return template('search', stable=final_table, htable=history_table)

run(app=app, host='localhost', port=8080, debug=True)