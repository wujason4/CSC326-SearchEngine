# from bottle import route, template, run, static_file
from bottle import *
import collections
import re

############
#  TO DO:  #
############
# - decide whether to store history as DEQUEUE or ORDEREDDICT
# - change all of the .format() to f-string

history = collections.OrderedDict()
HISTORY_MAX_LENGTH = 20

# Home Page
@route('/')
def home_page():
	pic = 'logo.png'
	return template('home_page', picture=pic)

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


run(host='localhost', port=8080, debug=True)
