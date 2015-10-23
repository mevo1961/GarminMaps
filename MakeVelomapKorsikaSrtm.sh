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
LEFT=8.5
RIGHT=9.6
BOTTOM=41.3
TOP=43.1
FAMID=1871
MAPNAME=OSM_Velo_Korsika
MAPID=6800
SRTM10ID=7800
SRTM20ID=7850
SRTMFAM10=2871
SRTMFAM20=2873
SRTM10MAPNAME=srtm10_korsika
SRTM20MAPNAME=srtm20_korsika
SCRIPT_DIR=/data1/OSM_Tools/scripts

if [[ -n ${CONTOURS} && -e ${CONTOURS} ]]
then
   CONTOPTION="-c ${CONTOURS}"
fi

# CONTOPTION="-z" # comment this away if you want contourlines

${SCRIPT_DIR}/MakeVelomapSrtm.sh -i ${INFILE} -l ${LEFT} -r ${RIGHT} -b ${BOTTOM} -t ${TOP} \
-f ${FAMID} -n ${MAPNAME} -o ${MAPID} -p ${SRTM10ID} -q ${SRTM20ID} \
-x ${SRTMFAM10} -y ${SRTMFAM20} -u ${SRTM10MAPNAME} -v ${SRTM20MAPNAME} ${CONTOPTION} \
-g 10 -h 50 -j 100
