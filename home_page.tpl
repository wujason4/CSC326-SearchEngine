<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/home_page.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <title>WaWu Search</title>
</head>

<body>
    <a href="/"><img id="logo" src="/images/logo.png" height="120" width="180"></a>
    <div id="main_container">

        <h2 id="title">WaWu</h2>

            <form action="/search/&page_no=1" method="post">
                <input id="search_input" type="text" name="keywords" placeholder="Search.." style="background-image:url(/images/searchicon.png);background-repeat:no-repeat;background-position:3px,10px;background-size:32px,32px">
                <br>
                <br>
                <input id="button" type="submit" value="Search!"/>
            </form>
            
    </div>
    <br>
    <center>
            {{!logging}}
            <div id="status">
			    {{!status}}
            </div>
    </center>
    <br>
    <br>

 
</body>
</html>