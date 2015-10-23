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
LEFT=8.9
RIGHT=15.9
BOTTOM=45.5
TOP=48.3
FAMID=1305
MAPNAME=OSM_Ostalpen
MAPID=6100
SRTM10ID=2300
SRTM20ID=2350
SRTMFAM10=2513
SRTMFAM20=2515
SRTM10MAPNAME=srtm10_OAlp
SRTM20MAPNAME=srtm20_OAlp
SCRIPT_DIR=/data1/OSM_Tools/scripts

${SCRIPT_DIR}/MakeGarmin.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} \
-g 20 -h 100 -j 500
