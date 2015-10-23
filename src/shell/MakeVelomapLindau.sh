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
LEFT=5.7
RIGHT=15.1
BOTTOM=47.2
TOP=55.2
FAMID=1771
MAPNAME=OSM_Velo_Hoki
MAPID=6700
SRTM10ID=7700
SRTM20ID=7750
SRTMFAM10=2771
SRTMFAM20=2773
SRTM10MAPNAME=srtm10_malle
SRTM20MAPNAME=srtm20_malle
SCRIPT_DIR=/data1/OSM_Tools/scripts

if [[ -n ${CONTOURS} && -e ${CONTOURS} ]]
then
   CONTOPTION="-c ${CONTOURS}"
fi

CONTOPTION="-z" # comment this away if you want contourlines

${SCRIPT_DIR}/MakeVelomap.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} ${CONTOPTION} \
-g 10 -h 50 -j 100
