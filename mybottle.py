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
current_status = 'visitor'
HISTORY_MAX_LENGTH = 20
SCOPES = ['https://www.googleapis.com/auth/plus.me ','https://www.googleapis.com/auth/userinfo.email']

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True
}

app = SessionMiddleware(app(),session_opts)
user_searchHistory = collections.OrderedDict()

# Home Page
@route('/',method=['GET','POST'])
def home_page():
	session = request.environ.get('beaker.session')
	
	user_email = session['user_email'] if 'user_email' in session else False
	user_name = session['user_name'] if 'user_name' in session else ''
	user_pic = session['user_pic'] if 'user_pic' in session else ''
	user_history = user_searchHistory[email] if email in user_searchHistory else None

	global current_status
	login = "<form action=\"/login\" method=\"get\"><input id=\"button_login\" type=\"submit\" value=\"login\"/></form>"
	logout = "<form action=\"/logout\" method=\"get\"><input id=\"button_logout\" type=\"submit\" value=\"logout\"/></form>"
	status_arg = "<p align=""center"">status: %s</p>" % current_status

	pic = 'logo.png'
	if current_status != 'visitor':
		log_arg = logout
	else:
		log_arg = login
	return template('home_page', logging = log_arg, status = status_arg, picture=pic)


# Static CSS file for the home_page table
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/login','GET')
def login():
	print "signing in"
	global current_status
	current_status = 'user'
	session = request.environ.get('beaker.session')
	flow = flow_from_clientsecrets("client_secrets.json",
						scope= SCOPES, 
						redirect_uri="http://localhost:8080/redirect")
	uri = flow.step1_get_authorize_url()
	return redirect(str(uri))
	
@route ('/logout')
def logout():
	session = request.environ.get('beaker.session')
	session.delete()
	global current_status
	current_status = 'visitor'
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
	
	session = request.environ.get('beaker.session')
	session['user_email'] = user_document['email']
	session['user_name'] = user_document['name']
	session['pic'] = user_document['picture']

	# After logging in go back to home page
	redirect('/')


@post('/search')
def show_results(stable='', htable=''):
		history = collections.OrderedDict()
		session = request.environ.get('beaker.session')
		user_email = session['user_email'] if 'user_email' in session else ''
		global current_status, logout, login 
		if user_email not in user_searchHistory:
			user_searchHistory[user_email] = collections.OrderedDict()
		
		# If logged in, use the history from user_searchHistory and add to that
		# Else, reset history 
		if current_status != 'visitor':
			user_history = user_searchHistory[user_email]
		else:
			visitor_history = collections.OrderedDict()

		# Get the search string
		original_string = request.forms.get('keywords')
		
		# Initialize the dictionary of unique words
		keyword_set = dict()
		checked = []

		# Extract whole words from the search string, may include repeats
		# **Should return ['word1', 'word2', 'word3']

		string = original_string.split()
		
		# Extract all unique words and store with count
		for word in string:

			regex = r"\b" + re.escape(word) + r"\b"
			count = sum(1 for match in re.finditer(regex, original_string))

			if word not in keyword_set:
				keyword_set[word] = count
					
		print "HISTORY_LENGTH: ", len(history)

		if current_status != 'visitor':
			sorted_history = sort_search(user_history, keyword_set)
		else:
			sorted_history = sort_search(visitor_history,keyword_set)

		##############################	
		# Create the table!! #
		##############################
		# 1) Style the table firsts
		final_table = "<table>"
		history_table = "<table>"
		
		# 2) Add the table heading
		final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>".format(original_string)
		history_table += "<thead><tr><th colspan=\"2\">Top 20 Searched</th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>"
		final_table, history_table = create_table(final_table, history_table, sorted_history, keyword_set)
		
		login = "<form action=\"/login\" method=\"get\"><input id=\"button_login\" type=\"submit\" value=\"login\"/></form>"
		logout = "<form action=\"/logout\" method=\"get\"><input id=\"button_logout\" type=\"submit\" value=\"logout\"/></form>"
		status_arg = "<p align=""center"">status: %s</p>" % current_status

		if current_status != 'visitor':
			log_arg = logout
		else:
			log_arg = login
		return template('search', logging=log_arg, status = status_arg, stable=final_table, htable=history_table)

def sort_search(history, keyword_set):
# For every unique searched word
	for s_word, s_count in keyword_set.items():

		# Check if word already in history
		if s_word in history:
			history[s_word] += s_count
		
		# word not in history, delete an entry from history and add new word
		else:

			# Check if user history has reached max length
			if len(history) < HISTORY_MAX_LENGTH:
				history[s_word] = s_count

			else:
				min_searched_count = min(history.values())

				# Delete min searched word
				for h_word, h_count in history.items():

					if h_count == min_searched_count:
						del history[h_word]
						break

				# Add newly searched to user history
				history[s_word] = s_count

	# Sort histrory in DESCENDING order
	sorted_history = collections.OrderedDict(sorted(history.iteritems(), key=lambda (k,v): (v,k), reverse=True))
	return sorted_history

def create_table(final_table,history_table, sorted_history, keyword_set):

	#Add the table data
	for i in keyword_set:
		final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

	for key, value in sorted_history.iteritems():
		history_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)


	#Close off the table
	final_table = final_table + "</tbody></table>"
	history_table = history_table + "</tbody></table>"

	return final_table, history_table


run(app=app, host='localhost', port=8080, debug=True)