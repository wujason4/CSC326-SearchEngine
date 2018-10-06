<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/table.css">
    <title>CSC326 - Lab1</title>
</head>
<body>
    <h2 id="logo" align="center">JDubbs Search Engine 1.0</h2>

    <p align="center">
        Please type in a search string below!
    </p>

    <br>
    <br>
    <form id="search_input" action="/results" method="post">
        <input type="text" name="keywords">
        <input id="button" type="submit" value="Search!"/>
    </form>
    
    <br>
    <br>

 
</body>
</html>