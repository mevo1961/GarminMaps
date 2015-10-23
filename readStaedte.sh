#! /bin/bash

if [[ ! -e staedte.txt ]]
then
   echo "Error: input file staedte.txt not found!"
   exit 1
fi

exec < staedte.txt


while read stadt left right bottom top
do
   if [[ $stadt == ${1}* ]]
   then
      echo $stadt $left $right $bottom $top
      found=1
   fi
done

if [[ -z "$found" ]]
then 
   echo "Sorry, the town $1 is not in our list!"
fi
