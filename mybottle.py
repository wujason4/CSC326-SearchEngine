# from bottle import route, template, run, static_file
from bottle import *
import collections

############
#  TO DO:  #
############
# - decide whether to store history as DEQUEUE or ORDEREDDICT
# - change all of the .format() to f-string

history = collections.OrderedDict()

# Home Page
@route('/')
def home_page():
    return template('home_page')

# Static CSS file for the home_page table
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@post('/search')
def show_results(stable='', htable=''):
		# Get the search string
		original_string = request.forms.get('keywords')
		
		# Initialize the dictionary of unique words
		keyword_set = dict()
		global history
		checked = []

		# Extract whole words from the search string
		# **Should return ['word1', 'word2', 'word3']
		string = original_string.split()
		
		# Iterate through every word in the search string
		for word in string:
			if not word in checked:
				checked.append(word)

				regex = r"\b" + re.escape(word) + r"\b"
				count = sum(1 for match in re.finditer(regex, original_string))
				
				if len(history) < 20:

					if word not in keyword_set:
						keyword_set[word] = count


					if word in history:
						print "\n\ncount in 1: ", count
						history[word] += count
					else:
						history[word] = count


				# History list already has 20 words, find least searched
				else:
					min_searched_count = min(history.keys())
					
					for x in history:
						if history[x] == min_searched_count:
							del history[x]
							break

					if word in history:
						print "\n\ncount in 2: ", count
						history[word] += count
					else:
						history[word] = count


		# Sort histrory in DESCENDING order
		sorted_history = collections.OrderedDict(sorted(history.iteritems(), key=lambda (k,v): (v,k), reverse=True))


		##############################	
		# Create the table!! #
		##############################
		# 1) Style the table firsts
		final_table = "<table align=\"center\" style=\"text-align:center;\">"
		history_table = "<table align=\"center\" style=\"text-align:center;\">"
		
		# 2) Add the table heading
		final_table += "<thead><tr><th colspan=\"2\">Searched for: <i>\"{}\"</i></th></tr></thead><tbody>".format(original_string)
		history_table += "<thead><tr><th colspan=\"2\">Top 20 Searched</th></tr></thead><tbody>"


		# 3) Add the table data
		for i in keyword_set:
			final_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(i, keyword_set[i])

		for key, value in sorted_history.iteritems():
			history_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)


		# 4) Close off the table
		final_table = final_table + "</tbody></table>"
		history_table = history_table + "</tbody></table>"


		return template('search', stable=final_table, htable=history_table)


run(host='localhost', port=8080, debug=True)
