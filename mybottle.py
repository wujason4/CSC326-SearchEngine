from bottle import *
import collections
import re
import httplib2
import sqlite3 as lite
import operator 
from beaker.middleware import SessionMiddleware
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

############
#  TO DO:  #
################################################################
# - decide whether to store history as DEQUEUE or ORDEREDDICT  #
################################################################

###################################################################################
# Temp list for database results:
# db_URLs = ["http://www.google.ca", "http://www.apple.com", "http://www.facebook.com", "http://www.fakenews.inc"]
# db_URLs = []
###################################################################################

#####################
#  INITIALIZATIONS  #
#####################

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


# For logging in
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


@post('/search/&page_no=<page_num:int>')
def show_results(page_num):
	global db_URLs

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
				
	if current_status != 'visitor':
		sorted_history = sort_search(user_history, keyword_set)
	else:
		sorted_history = sort_search(visitor_history,keyword_set)

	###################
	# Get the URLs
	###################

	# Extract first word searched
	first_word = string[0]

	# Call helper function to get all URLs
	urls = get_urls(first_word)

	for url in urls:
		print url
	print "==================type: ", type(urls)

	# Divide the URLs into page numbers
	page_no_urls = {}
	count = 0
	pg_num = 1


	for url in urls:
		if count == 5:
			pg_num += 1

		page_no_urls[url[0]] = pg_num
		count += 1

	print "\n\n DEBUG PRINT"
	for url, pg in page_no_urls.items():
		print url, pg
	# print page_no_urls
	print "SEARCHED WORD IS: ", first_word

	print "\n\nPAGE NUM IS: ", page_num
	# print "=================="


	db_URLs = []

	for url, pg in page_no_urls.items():
		if pg == page_num:
			db_URLs.append(url)

	print db_URLs


	##############################	
	# Create the table!! #
	##############################
	# 1) Style the table firsts
	final_table = "<table class=\"user_table\">"
	history_table = "<table class=\"user_table\">"
	url_table = "<table class=\"url_table\">"

	# Extra for navigation list
	nav_table = "<ul>"
	for i in range(page_num):
		nav_table += "<li><a href=\"/search/&page_no={}\"> 1 </a></li>".format(i+1)
	nav_table += "</ul>"
	
	# 2) Add the table heading
	final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>".format(original_string)
	history_table += "<thead><tr><th colspan=\"2\">Top 20 Searched</th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>"
	url_table += "<thead><tr><th colspan=\"2\">Result URLs</th></tr><tr><td>Link #</td><td>URL</td></tr></thead><tbody>"
	final_table, history_table, url_table = create_table(final_table, history_table, url_table, sorted_history, keyword_set, db_URLs)
	
	login = "<form action=\"/login\" method=\"get\"><input id=\"button_login\" type=\"submit\" value=\"login\"/></form>"
	logout = "<form action=\"/logout\" method=\"get\"><input id=\"button_logout\" type=\"submit\" value=\"logout\"/></form>"
	status_arg = "<p>status: %s</p>" % current_status

	if current_status != 'visitor':
		log_arg = logout
	else:
		log_arg = login

	return template('search', logging=log_arg, status=status_arg, s_table=final_table, h_table=history_table, db_from=url_table, n_table=nav_table)



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

def create_table(final_table, history_table, url_table, sorted_history, keyword_set, db_URLs):

	# Add table data for search
	for i in keyword_set:
		final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

	# Add table data for history
	for key, value in sorted_history.iteritems():
		history_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)

	# Add table data for URLs
	for index, url in enumerate(db_URLs):
		url_table += "<tr><td>{}</td><td><a href=\"{}\">{}</a></td></tr>\n".format(index+1, url, url)


	#Close off the table
	final_table += "</tbody></table>"
	history_table += "</tbody></table>"
	url_table += "</tbody></table>"

	return final_table, history_table, url_table

def get_urls(keyword):

	# Load the DB
	db = lite.connect("backend/dbFile.db")
	
	cur = db.cursor()
	page_url_score = { }
	#t = "\'%"+keyword+"%\'"
	# Get word_id from lexicon table
	#cur.execute("SELECT word_id FROM lexicon WHERE word like ?",(t,))
	cur.execute("SELECT word_id FROM lexicon WHERE word =?",(keyword,))
	word_id = cur.fetchone()

	# Get all doc_id's from inverted_index table
	cur.execute("SELECT doc_id FROM inverted_index WHERE word_id = ?", (word_id[0],))
	doc_id_list = cur.fetchone()

	# Convert list into string
	doc_id_list_string = str(doc_id_list[0])
	

	# Iterate through all doc_id's and find corresponding URL and page rank score
	# Save as dictionary ==> {"url": "score"}
	for doc_id in doc_id_list_string.split(","):

		# Get URL for current doc_id
		cur.execute("SELECT url FROM document_index WHERE doc_id = ?",(doc_id,))
		page_url = cur.fetchone()
		url_str = str(page_url[0])

		# Get page rank score for each URL
		cur.execute("SELECT rank_score FROM page_rank_score WHERE doc_id = ?", (doc_id,))
		page_rank = cur.fetchone()
		
		print "==========566666==========="
		print url_str
		print page_rank[0] 
		print "===========566666=========="

		if page_rank is not None:
			page_url_score[url_str] = page_rank

	sorted_url_score = sorted(page_url_score.items(), key=operator.itemgetter(1), reverse = True)
	return sorted_url_score

##################
# ERROR HANDLING #
##################
@error(404)
def error_handler_404(error):
	pic = 'logo.png'
	return template('error_handler')

@error(500)
def error_handler_404(error):
	pic = 'logo.png'
	return template('error_handler')



# Local run
run(app=app, host='localhost', port=8080, debug=True)

# AWS run
# run(app=app, host='0.0.0.0', port=80, debug=True)
