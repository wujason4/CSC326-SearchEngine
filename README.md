# CSC326-SearchEngine
==========================
Lab 2:
==========================
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

==========================
LAB 3:
==========================

Backend:
To run backend, run command "python crawler.py"
For test script: (see read me file under backend folder)
	1. run "python mybottle.py"
	2. run "python run_backend_test.py"



Frontend:
 - Public DNS ==> http://http://100.26.143.194:80/

 - benchmark command ==> ab -n 1000 -c 15 http://100.26.143.194:80/?keywords=google results see below:

This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 100.26.143.194 (be patient)


Server Software:        WSGIServer/0.1
Server Hostname:        100.26.143.194
Server Port:            80

Document Path:          /?keywords=google
Document Length:        952 bytes

Concurrency Level:      15
Time taken for tests:   6.347 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      1232000 bytes
HTML transferred:       952000 bytes
Requests per second:    157.56 [#/sec] (mean)
Time per request:       95.204 [ms] (mean)
Time per request:       6.347 [ms] (mean, across all concurrent requests)
Transfer rate:          189.56 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       34   38   3.2     38      58
Processing:    38   47  30.1     43     326
Waiting:       36   46  29.9     42     326
Total:         72   86  30.4     81     367

Percentage of the requests served within a certain time (ms)
  50%     81
  66%     83
  75%     84
  80%     86
  90%     91
  95%    100
  98%    108
  99%    338
 100%    367 (longest request)


 **Difference in results due to overhead in accessing data base and retrieving/parsing/organizing database results.