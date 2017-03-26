set terminal png

set output "benchmark.png"

set title "ab -n 100 -c 50 -g out.data http:127.0.0.1:5000/"

set size 1,0.7

set grid y

set xlabel "request"

set ylabel "response time (ms)"

plot "out.data" using 4 smooth sbezier with lines title "something"
