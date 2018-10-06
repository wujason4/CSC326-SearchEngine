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

@post('/results')
def show_results(table=''):
		# Get the search string
		original_string = request.forms.get('keywords')
		
		# Initialize the dictionary of unique words
		keyword_set = dict()

		# Extract whole words from the search string
		# **Should return ['word1', 'word2', 'word3']
		string = original_string.split()
		
		# Iterate through every word in the search string
		for word in string:
			regex = r"\b" + re.escape(word) + r"\b"
			count = sum(1 for match in re.finditer(regex, original_string))
			if word not in keyword_set:
				keyword_set[word] = count
		
		######################	
		# Create the table!! #
		######################
		# 1) Style the table first
		final_table = "<table align=\"center\" style=\"text-align:center;\">"
		
		# 2) Add the table heading
		final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr></thead><tbody>".format(original_string)

		# 3) Add the table data
		for i in keyword_set:
			final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

		# 4) Close off the table
		final_table = final_table + "</tbody></table>"


		return template('results', table=final_table)



run(host='localhost', port=8080, debug=True)
