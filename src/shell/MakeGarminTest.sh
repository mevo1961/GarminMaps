#!/bin/bash

# Startmeldung geben und Parameter / Optionen prüfen
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
LEFT=9.700
RIGHT=9.900
BOTTOM=47.40
TOP=47.55
FAMID=1555
MAPNAME=OSM_Lindau
MAPID=6666
SRTM10ID=2500
SRTM20ID=2550
SRTMFAM10=2521
SRTMFAM20=2523
SRTM10MAPNAME=srtm10_bay
SRTM20MAPNAME=srtm20_bay
SCRIPTDIR=/data1/OSM_Tools/scripts

${SCRIPTDIR}/MakeGarmin.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} \
-g 20 -h 100 -j 500 -z
