<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/results.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <script src="/scripts/toggle.js"></script>
    <title>WaWu Search</title>
</head>

<body>

<!-- HEADER CONTAINER -->

    <div id="header_container">
        <div id="logo_container">
            <h2 id="title">
                WaWu
            </h2>  
            <a href="/"><img id="logo" src="/images/logo.png" height="120" width="180"></a>
        </div>
        <div id="search_container">
            <form action="/search/&page_no=1" method="post">
            <!-- <form action="/search" method="post"> -->
                <input id="search_input" type="text" name="keywords" placeholder="Search.." style="background-image:url(/images/searchicon.png);background-repeat:no-repeat;background-position:3px,10px;background-size:32px,32px">
                <input id="search_button" type="submit" value="Search!"/>
            </form>
        </div>
        <div id="login_container">
            {{!logging}}
            <div id="status">
                {{!status}} 
            </div>
        </div>
    </div>

    <br>
    <br>
    <br>

    <!-- <h1>THIS IS PAGE {{page_num}}</h1> -->
    
    <div id="history_toggle" style="font-family: 'Open Sans', sans-serif">
        <form onclick='myFunction()'>
            History <input id="history_checkbox" type="checkbox"/>
        </form>
    </div>
    


    
    <!-- <button onclick="myFunction()">History</button> -->
      
    <div id="user_table_container">

        <div class="history_table">
            {{!h_table}}
        </div>
    </div>


    


    


<!-- DISPLAY RESULTS HERE -->
    
    <div id="results_container">
        <center>
            <div class="url_table">
                {{!db_from}}
            </div>
        </center>
    </div>

    <br>
    <br>
    

<!-- PAGE NAVIGATION HERE -->


    <div id="navigation_container">
        <center>
            <div class="nav_list">
                {{!n_table}}
            </div>
        </center>
    </div>
    
</body>
</html>
