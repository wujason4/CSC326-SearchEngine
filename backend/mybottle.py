# from bottle import route, template, run, static_file
from bottle import *

# Home Page
@route('/')
def home_page():
    return template('frontend_template')

@route('/page1.tpl')
def test_page():
    return template('page1')

@route('/page2.tpl')
def test_page():
    return template('page2')
@route('/page3.tpl')
def test_page():
    return template('page3')
# Static CSS file for the home_page table
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')


run(host='localhost', port=8080, debug=True)
