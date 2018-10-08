<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/table.css">
    <title>CSC326 - Lab1</title>
</head>
<body>
    <h2 id="logo" align="center">JDubbs Search Engine 1.0</h2>

    <br>
    <br>
    <div>
        <form action="/search" method="post">
            <input id="search_input" type="text" name="keywords">
            <br>
            <br>
            <input id="button" type="submit" value="Search!"/>
        </form>
    </div>
    <br>

    <br>
    <br>
    {{!stable}}
    <br>
    <br>
    {{!htable}}
     
<!--      <table align="center" style="text-align:center;" >
        <thead>
            <tr>
                <th colspan="2">
                    Searched for: {{str}}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Key Word</td>
                <td>Number of Times</td>
            </tr>
        </tbody>
    </table> -->

<!--     <form action="/">
        <input type="submit" value="Go back home!"/>
    </form> -->

    <br>
    <br>
    

</body>
</html>