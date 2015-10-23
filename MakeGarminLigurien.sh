#!/bin/bash

# Startmeldung geben und Parameter / Optionen prüfen
echo $$: $0 "$*"
while getopts ":i:c:" OPT
do
   case $OPT in
   i ) INFILE=${OPTARG} ;;
   c ) CONTOURS=${OPTARG} ;;
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
LEFT=7.70
RIGHT=10.5
BOTTOM=43.8
TOP=45.50
FAMID=1445
MAPNAME=OSM_Ligurien
MAPID=6600
SRTM10ID=7600
SRTM20ID=7650
SRTMFAM10=2631
SRTMFAM20=2633
SRTM10MAPNAME=srtm10_ligurien
SRTM20MAPNAME=srtm20_ligurien
SCRIPT_DIR=/data1/OSM_Tools/scripts

${SCRIPT_DIR}/MakeGarmin.sh -i ${INFILE} -c ${CONTOURS} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} \
-g 10 -h 50 -j 100
