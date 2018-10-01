# from bottle import route, template, run, static_file
from bottle import *

# Home Page
@route('/')
def home_page():
    return template('frontend_template')

# Static CSS file for the home_page table
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

# Results Page
@get('/results')
def show_results_get():
	return

@post('/results')
def show_results(param=''):
		string = request.forms.get('keywords')

		# return "<p>This is your search string %s.</p>" %(string)
		return template('results', param=string)


run(host='localhost', port=8080, debug=True)
