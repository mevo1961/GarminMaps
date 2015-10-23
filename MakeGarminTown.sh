#!/bin/bash

# Startmeldung geben und Parameter / Optionen prüfen
echo $$: $0 "$*"
SCRIPT_DIR=/data1/OSM_Tools/scripts

while getopts ":i:s:" OPT
do
   case $OPT in
   i ) INFILE=${OPTARG} ;;
   s ) TOWN=${OPTARG} ;;
   * ) echo "Invalid Option" ;;
   esac
done
if [[ -z $INFILE ]] 
then
   echo "you must specify an input file!"
   exit 1
else
   echo "Infile: $INFILE"
fi
if [[ -z $TOWN ]] 
then
   echo "you must specify a town!"
   exit 1
else
   echo "Town: $TOWN"
fi

if [[ ! -e ${SCRIPT_DIR}/towns.txt ]]
then
   echo "Error: input file ${SCRIPT_DIR}/towns.txt not found!"
   exit 1
fi

exec < ${SCRIPT_DIR}/towns.txt


while read TO LEFT RIGHT BOTTOM TOP FAMID MAPID
do
   if [[ $TO == ${TOWN}* ]]
   then
      echo ${TOWN} ${LEFT} ${RIGHT} ${BOTTOM} ${TOP} ${FAMID} ${MAPID}
      found=1
      break
   fi
done

if [[ -z "$found" ]]
then 
   echo "Sorry, the town $1 is not in our list!"
fi

MAPNAME=OSM_${TOWN}

${SCRIPT_DIR}/MakeGarmin.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
 -f ${FAMID} -n ${MAPNAME} -o ${MAPID}  -z 
