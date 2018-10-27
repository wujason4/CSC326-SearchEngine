string = """/<!DOCTYPE html/>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/search.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <title>WaWu Search</title>
</head>

<body>
    <img id="logo" src="/static/logo.png" height="120" width="180">
    <div id="main_container">

        <h2 id="title">WaWu</h2>

            <form action="/search" method="post">
                <input id="search_input" type="text" name="keywords">
                <br>
                <br>
                <input id="button" type="submit" value="Search!"/>
            </form>
            
    </div>
    <br>
    <p align="center">
		    <a href="login">Sign in</a>
    </p>
    <br>
    <br>

 
</body>
</html>"""

first_part = string.split("<body>",1)[0]
second_part = string.split("<body>",1)[1]

new_line = """<p>login status: JEN</p>"""
new_string = first_part + new_line + second_part
print new_string