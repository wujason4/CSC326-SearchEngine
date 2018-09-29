from bottle import route, template, run, static_file

@route('/')
def home_page():
    return template('frontend_template')

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

run(host='localhost', port=8080, debug=True)
