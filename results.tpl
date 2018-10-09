<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/table.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <title>WaWu Search</title>
</head>

<body>

    <img id="logo" src="/static/logo.png" height="120" width="180">
    <div>

        <h2 id="title">WaWu</h2>

            <form action="/search" method="post">
                <input id="search_input" type="text" name="keywords">
                <br>
                <br>
                <input id="button" type="submit" value="Search!"/>
            </form>
    </div>

    <br>
    <br>
    {{!table}}
    <br>
    <br>
     
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

    <form action="/">
        <input type="submit" value="Go back home!"/>
    </form>

    <br>
    <br>
    

</body>
</html>