<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="/static/table.css">
    <title>CSC326 - Lab1</title>
</head>
<body>
    <h2>JDubbs Search Engine 1.0</h2>

    <p align="center">
        This is the results page...
    </p>
     
     <table align="center" style="text-align:center;" >
        <thead>
            <tr>
                <th colspan="2">
                    Search for: {{param}}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>The table body</td>
                <td>With two Columns</td>
            </tr>
        </tbody>
    </table>

    <form action="/">
        <input type="submit" value="Go back home!"/>
    </form>

    <br>
    <br>
    

</body>
</html>