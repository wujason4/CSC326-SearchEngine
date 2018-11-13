<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/results.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <title>WaWu Search</title>
</head>

<body>

<!-- HEADER CONTAINER -->

    <div id="header_container">
        <div id="logo_container">
            <h2 id="title">
                WaWu
            </h2>  
            <img id="logo" src="/static/logo.png" height="120" width="180">
        </div>
        <div id="search_container">
            <form action="/search/&page_no=1" method="post">
                <input id="search_input" type="text" name="keywords">
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

    <div id="user_table_container">
        <div class="search_table">
            {{!s_table}}
        </div>
        <div class="history_table">
            {{!h_table}}
        </div>
    </div>

    <br>
    <br>

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
                <!-- <ul>
                    <li><a href="prev">Prev</a></li>
                    <li><a href="1"> 1 </a></li>
                    <li><a href="2"> 2 </a></li>
                    <li><a href="3"> 3 </a></li>
                    <li><a href="4"> 4 </a></li>
                    <li><a href="5"> 5 </a></li>
                    <li><a href="next">Next</a></li>
                </ul> -->

                {{!n_table}}

            </div>
        </center>
    </div>
    
</body>
</html>

<!--
<!DOCTYPE html>
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
    <center>
        {{!logging}}
        {{!status}}
    </center>
   
    <br>

    <br>
    <br>
    <div>
        <div id="search_table">
            {{!s_table}}
        </div>

        <div id="history_table">
            {{!h_table}}
        </div>
    </div>
    <br>

    <div id="url_list">
        <center>
            <p>This is where the URLs will go: </p>

            {{!db_from}}
        </center>
    </div>

</body>
</html>

 -->
