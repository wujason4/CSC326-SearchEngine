<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/table.css">
    <title>CSC326 - Lab1</title>
</head>
<body>
    <h2>JDubbs Search Engine 1.0</h2>

    <p>
        Please type in a search string below!
    </p>

<!--     <form action="display.py">
 -->        


    <form action="/results" method="post">
        Type Here: <input type="text" name="keywords" />
        <input type="submit" value="Search!"/>
    </form>

    <br>
    <br>
    

</body>
</html>