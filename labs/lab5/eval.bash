#!/bin/bash

printf "n,LASTBOW,LOSTWORLD,OTHERS\n"

for n in 1 2 3 4 5 6 7 8 9
do
    ngram-count -order $n -text $1 -$2 $3 -lm tmp.lm

    bow=`ngram -order $n -lm tmp.lm -ppl his-last-bow.tok.txt | egrep -o "ppl= [0-9.]+" | egrep -o "[0-9.]+"`
    world=`ngram -order $n -lm tmp.lm -ppl lost-world.tok.txt | egrep -o "ppl= [0-9.]+" | egrep -o "[0-9.]+"`
    others=`ngram -order $n -lm tmp.lm -ppl other-authors.tok.txt | egrep -o "ppl= [0-9.]+" | egrep -o "[0-9.]+"`
    
    rm -f tmp.lm
    printf "$n,$bow,$world,$others\n"
done

