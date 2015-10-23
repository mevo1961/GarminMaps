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
LEFT=-2.5
RIGHT=7.8
BOTTOM=42.2
TOP=45.00
# TOP=47.00
FAMID=1443
MAPNAME=OSM_Sfrkr
MAPID=6500
SRTM10ID=2700
SRTM20ID=2750
SRTMFAM10=2531
SRTMFAM20=2533
SRTM10MAPNAME=srtm10_sfrkr
SRTM20MAPNAME=srtm20_sfrkr
SCRIPT_DIR=/data1/OSM_Tools/scripts

${SCRIPT_DIR}/MakeGarmin.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} \
-g 10 -h 50 -j 100
