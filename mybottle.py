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


"""
###########################
#      FEATURE TO DO:     #
###########################
- toggle button for dark theme
DONE- add search icon into search bar
- toggle button to show recent search history
- spellcheck
	- can also create a dictionary feature
- calculator
DONE- multi-word search 

"""


############################
#  GLOBAL INITIALIZATIONS  #
############################

# Backend
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


# Frontend
# final_table = None
history_table = None
url_table = None
nav_table = None
page_no_urls = collections.OrderedDict()
MAX_PAGES = 1



############################
#          ROUTING         #
############################

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


@route('/search', defaults={'page_num', 1})
@route('/search/&page_no=<page_num:int>' or '/search/%26page_no%3D<page_num:int>', method=['GET', 'POST'])
def show_results(page_num):

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
	query_string = request.forms.get('keywords')

	# Make sure only modifying global variables
	# global final_table
	global history_table
	global url_table
	global nav_table
	global page_no_urls
	global MAX_PAGES


	# Check if new search query
	if not query_string:
		db_URLs = []

		for url, pg in page_no_urls.items():
			if pg == page_num:
				db_URLs.append(url)


		#############################	
		#     Create the table!!    #
		#############################
		
		# 1) Style the table firsts
		url_table = "<table class=\"url_table\">"
		
		# 2) Add the table heading
		url_table += "<thead><tr><th colspan=\"2\">Result URLs</th></tr><tr><td>Link #</td><td>URL</td></tr></thead><tbody>"
		url_table = fill_URL_table(db_URLs, page_num)

		# 3) Add table contents
		nav_table = fill_pagination(page_num, MAX_PAGES)

		# Check login status
		login = "<form action=\"/login\" method=\"get\"><input id=\"button_login\" type=\"submit\" value=\"login\"/></form>"
		logout = "<form action=\"/logout\" method=\"get\"><input id=\"button_logout\" type=\"submit\" value=\"logout\"/></form>"
		status_arg = "<p>status: %s</p>" % current_status

		if current_status != 'visitor':
			log_arg = logout
		else:
			log_arg = login

		return template('page_no', logging=log_arg, status=status_arg, h_table=history_table, db_from=url_table, n_table=nav_table, page_num=page_num)


	# NEW SEARCH
	elif query_string:

		# Set global variables back to default
		final_table = None
		history_table = None
		url_table = None
		nav_table = None
		page_no_urls = collections.OrderedDict()
		MAX_PAGES = 1
	
		# Initialize the dictionary of unique words
		keyword_set = dict()
		checked = []

		# Extract whole words from the search string, may include repeats
		# **Should return ['word1', 'word2', 'word3']
		string = query_string.split()
		
		# Extract all unique words and store with count
		for word in string:

			regex = r"\b" + re.escape(word) + r"\b"
			count = sum(1 for match in re.finditer(regex, query_string))

			if word not in keyword_set:
				keyword_set[word] = count

		if current_status != 'visitor':
			sorted_history = sort_search(user_history, keyword_set)
		else:
			sorted_history = sort_search(visitor_history,keyword_set)

		
		####################
		#   Get the URLs   #
		####################



		# Find all the common urls for multiple searched word
		list_of_urls = []
		common_urls = set()
		
		if len(keyword_set) ==1:

			# Extract first word searched
			first_word = string[0]

			# Get all URLs from DB
			common_urls = get_urls(first_word)

		if len(keyword_set) > 1:

			for word in keyword_set:
				urls = get_urls(word)
				for u in urls:
					list_of_urls.append(u)
			
			for s in range(0,len(list_of_urls)):
				for x in range (s+1,len(list_of_urls)):
					if list_of_urls[s]==list_of_urls[x]:
						common_urls.add(list_of_urls[s])

			common_urls = list(common_urls)

		sorted_common_urls = sorted(common_urls, key=operator.itemgetter(1), reverse = True)
		
		# Group URLs into its corresponding page number
		count = 0
		for url in sorted_common_urls:
			if count == 5:
				MAX_PAGES += 1
				count = 0
			page_no_urls[url[0]] = MAX_PAGES
			count += 1

		# Get URLs specific for the requested page number
		db_URLs = []
		print "------------------------"
		for url, pg in page_no_urls.items():
			
			print url
			if pg == page_num:
				db_URLs.append(url)


		########################	
		#   Create the table   #
		########################

		# 1) Style the table firsts
		# final_table = "<table class=\"user_table\">"
		history_table = "<table class=\"user_table\">"
		url_table = "<table class=\"url_table\">"
		
		# 2) Add the table heading
		# final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>".format(query_string)
		history_table += "<thead><tr><th colspan=\"2\">Top 20 Searched</th></tr><tr><td>Word</td><td>Count</td></tr></thead><tbody>"
		url_table += "<thead><tr><th colspan=\"2\">Result URLs</th></tr><tr><td>Link #</td><td>URL</td></tr></thead><tbody>"
		
		# 3) Add table contents
		history_table = fill_table(history_table, url_table, sorted_history, keyword_set)
		url_table = fill_URL_table(db_URLs, page_num)
		nav_table = fill_pagination(page_num, MAX_PAGES)


		# 4) Check login status
		login = "<form action=\"/login\" method=\"get\"><input id=\"button_login\" type=\"submit\" value=\"login\"/></form>"
		logout = "<form action=\"/logout\" method=\"get\"><input id=\"button_logout\" type=\"submit\" value=\"logout\"/></form>"
		status_arg = "<p>status: %s</p>" % current_status

		if current_status != 'visitor':
			log_arg = logout
		else:
			log_arg = login


		return template('page_no', logging=log_arg, status=status_arg, h_table=history_table, db_from=url_table, n_table=nav_table, page_num=page_num)



##########################
#   Serve static files   #
##########################
@route('/images/<filename>')
def server_static_images(filename):
    return static_file(filename, root='./images')

@route('/static/<filename>')
def server_static_css(filename):
	return static_file(filename, root='./static')

# @route('/template/<filename>')
# def server_static_templates(filename):
# 	return static_file(filename, root='./template')



##################
#   USER LOGIN   #
##################
@route('/login','GET')
def login():
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



############################
#     HELPER FUNCTIONS     #
############################

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


def fill_table(history_table, url_table, sorted_history, keyword_set):

	# Add table data for search
	# for i in keyword_set:
	# 	final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

	# Add table data for history
	for key, value in sorted_history.iteritems():
		history_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)


	# Close off the table
	# final_table += "</tbody></table>"
	history_table += "</tbody></table>"

	return history_table


def fill_URL_table(db_URLs, page_num):
	
	global url_table

	# Add table data for URLs
	for index, url in enumerate(db_URLs):
		url_table += "<tr><td>{}</td><td><a href=\"{}\">{}</a></td></tr>\n".format(index+1, url, url)

	# Close off the table
	url_table += "</tbody></table>"

	return url_table


def fill_pagination(page_num, MAX_PAGES):

	# Create list header
	nav_table = "<ul>"

	# Add "Prev" button
	if page_num > 1:
		nav_table += "<li><a href=\"/search/&page_no={}\"> Prev </a></li>".format(page_num - 1)
	else:
		nav_table += "<li><a href=\"/search/&page_no={}\"> Prev </a></li>".format(1)

	# Add page numbers
	for i in range(MAX_PAGES):
		if i+1 == page_num:
			nav_table += "<li style=\"background-color:rgba(0, 128, 0, 0.55)\"><a href=\"/search/&page_no={}\"> {} </a></li>".format(i+1, i+1)
		else:
			nav_table += "<li><a href=\"/search/&page_no={}\"> {} </a></li>".format(i+1, i+1)
	
	# Add "Next" button
	if page_num < MAX_PAGES:
		nav_table += "<li><a href=\"/search/&page_no={}\"> Next </a></li>".format(page_num + 1)
	else:
		nav_table += "<li><a href=\"/search/&page_no={}\"> Next </a></li>".format(MAX_PAGES)

	# Close list
	nav_table += "</ul>"

	return nav_table


def get_urls(keyword):

	# Load the DB
	db = lite.connect("backend/dbFile.db")
	
	cur = db.cursor()
	page_url_score = { }
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

		if page_rank is not None:
			page_url_score[url_str] = page_rank[0]

	sorted_url_score = sorted(page_url_score.items(), key=operator.itemgetter(1), reverse = True)

	return sorted_url_score


#################
#ERROR HANDLING #
#################
@error(404)
def error_handler_404(error):
	pic = 'logo.png'
	return template('error_handler')

@error(500)
def error_handler_500(error):
	pic = 'logo.png'
	return template('error_handler')


# Local run
run(app=app, host='localhost', port=8080, debug=True)

# AWS run
# run(app=app, host='0.0.0.0', port=80, debug=True)
