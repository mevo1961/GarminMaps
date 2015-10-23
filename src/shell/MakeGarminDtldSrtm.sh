#!/bin/bash

# Startmeldung geben und Parameter / Optionen prüfen
echo $$: $0 "$*"
while getopts ":c:" OPT
do
   case $OPT in
   c ) CONTOURS=${OPTARG} ;;
   * ) echo "Invalid Option" ;;
   esac
done
LEFT=5.7
RIGHT=15.1
BOTTOM=47.2
TOP=55.2
SRTM10ID=7400
SRTM20ID=7450
SRTMFAM10=2441
SRTMFAM20=2442
SRTM10MAPNAME=srtm10_dtld
SRTM20MAPNAME=srtm20_dtld
SCRIPT_DIR=/data1/OSM_Tools/scripts

if [[ -n ${CONTOURS} && -e ${CONTOURS} ]]
then
   CONTOPTION="-c ${CONTOURS}"
fi

${SCRIPT_DIR}/MakeGarminSrtm.sh  -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-p ${SRTM10ID} -q ${SRTM20ID} ${CONTOPTION} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} \
-g 10 -h 50 -j 100
