# CSC326-SearchEngine
To run frontend run command "python mybottle.py"

On localhost:
When logging out, user can only login using same account as first login
Login info is not required again after first log in



=====================================================================
1) Web Server IP ==> http://34.204.9.40:80/

2) Benchmark Setup:
- used apache2-utils
- set 15 concurrent requests
- completed 1000 requests
- used following keywords: hello, foo, bar

** Executed Command ==> ab -n 1000 -c 15 http://34.204.9.40:80/?keywords=helloworld+foo+bar

