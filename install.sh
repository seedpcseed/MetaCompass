#!/usr/bin/env bash
 
echo "#Installing MetaCompass"
cmd="g++ -Wall -W -O2 -o ./bin/extractSeq ./src/utils/extractSeq.cpp"
echo $cmd
$cmd

cmd="g++ -Wall -W -O2 -o ./bin/formatFASTA ./src/utils/formatFASTA.cpp"
echo $cmd
$cmd
cmd="g++  -W -O2 -o ./bin/breadth ./src/utils/breadth.cpp -std=gnu++11"
echo $cmd
$cmd

cmd="g++ -Wall -W -O2 -o ./bin/extractContigs ./src/utils/extractContigs.cpp -std=gnu++11"
echo $cmd
$cmd

cmd="g++  -W -O2 -o ./bin/processmash ./src/utils/processmash.cpp -std=gnu++11"
echo $cmd
$cmd

cmd="g++ -Wall -W -O2 -o ./bin/fq2fa ./src/utils/fq2fa.cpp -std=gnu++11"
echo $cmd
$cmd

cmd="g++ -Wall -W -O2 -o ./bin/buildcontig ./src/buildcontig/buildcontig.cpp ./src/buildcontig/cmdoptions.cpp ./src/buildcontig/memory.cpp ./src/buildcontig/procmaps.cpp ./src/buildcontig/outputfiles.cpp"
echo $cmd
$cmd

#Updated Jan 14th 2020
#cmd="wget --no-check-certificate https://obj.umiacs.umd.edu/metacompassdb/refseq-2020-01-14.tar.gz"
#echo $cmd
#$cmd

#cmd="tar -xzvf refseq-2020-01-14.tar.gz"
#echo $cmd
#$cmd

#optional
#cmd="rm refseq-2020-01-14.tar.gz"
#echo $cmd
#$cmd

