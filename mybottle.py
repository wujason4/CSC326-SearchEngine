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



# # TESTING TABLE CREATOR #
# @route('/test')
# def test():
# 	return template('test')

# @post('/testResults')
# def test_results(par=''):
# 	num = int(request.forms.get('num_rows'))
# 	final_table = "<table><thead><tr><th colspan=\"2\">Wanted: " + str(num) + "rows</th></tr></thead><tbody>"

# 	for i in range(num):
# 		final_table = final_table + "<tr><td>Word</td><td>{}</td></tr>\n".format(i)

# 	final_table = final_table + "</tbody></table>"

# 	return template('test_results', par=final_table)




run(host='localhost', port=8080, debug=True)
