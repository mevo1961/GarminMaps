#!/bin/bash

# Startmeldung geben und Parameter / Optionen prüfen
echo $$: $0 "$*"
while getopts ":i:c:g:h:j:l:r:b:t:f:n:o:p:q:x:y:u:v:z" OPT
do
   case $OPT in
   b ) BOTTOM=${OPTARG} ;;
   c ) CONTOURS=${OPTARG} ;;
   f ) FAMID=${OPTARG} ;;
   g ) CSTEPMIN=${OPTARG} ;;
   h ) CSTEPMED=${OPTARG} ;;
   i ) INFILE=${OPTARG} ;;
   j ) CSTEPMAX=${OPTARG} ;;
   l ) LEFT=${OPTARG} ;;
   n ) MAPNAME=${OPTARG} ;;
   o ) MAPID=${OPTARG} ;;
   p ) SRTMMINID=${OPTARG} ;;
   q ) SRTMMAJID=${OPTARG} ;;
   r ) RIGHT=${OPTARG} ;;
   t ) TOP=${OPTARG} ;;
   u ) SRTMMINMAPNAME=${OPTARG} ;;
   v ) SRTMMAJMAPNAME=${OPTARG} ;;
   x ) SRTMFAMMIN=${OPTARG} ;;
   y ) SRTMFAMMAJ=${OPTARG} ;;
   z ) NOCONTOURS=YES ;;
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

# set some required variables
if [[ -z ${CSTEPMIN} ]]
then
   CSTEPMIN=10
fi
if [[ -z ${CSTEPMED} ]]
then
   CSTEPMED=50
fi
if [[ -z ${CSTEPMAX} ]]
then
   CSTEPMAX=100
fi
TYPFILE=${FAMID}.TYP
SRTMMINTYP=${SRTMFAMMIN}.TYP
SRTMMAJTYP=${SRTMFAMMAJ}.TYP
TOOL_DIR=$(pwd)
TYP_DIR=${TOOL_DIR}/typFiles
MKGMAP_DIR=$(ls ${TOOL_DIR} | grep mkgmap)
STYLES_DIR=${TOOL_DIR}/styleFiles
SPLITTER_DIR=$(ls ${TOOL_DIR} | grep splitter)
OSMOSIS_DIR=$(ls ${TOOL_DIR} | grep osmosis)
echo "using typfile ${TYPFILE}"
# increase heap for osmosis
export JAVACMD_OPTIONS=-Xmx1536M

# cut selected area from input file
echo "Cutting area from ${INFILE}: Left=${LEFT}, Right=${RIGHT}, Bottom=${BOTTOM},"
echo "Top=${TOP}"
${TOOL_DIR}/${OSMOSIS_DIR}/bin/osmosis --read-xml enableDateParsing=no \
${INFILE} --bounding-box left=$LEFT right=$RIGHT bottom=$BOTTOM  \
top=$TOP completeWays=no idTrackerType=BitSet --write-xml file=${TOOL_DIR}/temp.osm
if [[ ${INFILE} == *.bz2 ]]
then
   CAT_CMD=bzcat
else
   CAT_CMD=cat
fi
CMD="$CAT_CMD ${INFILE} | ${TOOL_DIR}/${OSMOSIS_DIR}/bin/osmosis --read-xml enableDateParsing=no \
file=/dev/stdin --bounding-box left=$LEFT right=$RIGHT bottom=$BOTTOM  \
top=$TOP completeWays=no idTrackerType=BitSet --write-xml file=${TOOL_DIR}/temp.osm"
echo "Executing ${CMD}"
eval ${CMD}

echo "splitting area into tiles ..."
CMD="java -Xmx2000M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar \
--mapid=${MAPID}0001 --max-nodes=800000 --max-areas=20 ${TOOL_DIR}/temp.osm"
eval ${CMD}

rm temp.osm

# patch Typfile
cp ${TYP_DIR}/Default.TYP ${TYP_DIR}/${TYPFILE}
${TOOL_DIR}/gmaptool/gmt -wy ${FAMID} ${TYP_DIR}/${TYPFILE}
cp ${TYP_DIR}/SRTM.TYP ${TYP_DIR}/${SRTMMINTYP}
${TOOL_DIR}/gmaptool/gmt -wy ${SRTMFAMMIN} ${TYP_DIR}/${SRTMMINTYP}
cp ${TYP_DIR}/SRTM.TYP ${TYP_DIR}/${SRTMMAJTYP}
${TOOL_DIR}/gmaptool/gmt -wy ${SRTMFAMMAJ} ${TYP_DIR}/${SRTMMAJTYP}

echo "creating basemap ..."
CMD="java -Xmx2000M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
--description=${MAPNAME} \
--style-file=${STYLES_DIR}/mkgmap-style-toponew_mevo/ \
--family-id=${FAMID} \
--product-id=1 \
--series-name=${MAPNAME} \
--family-name=${MAPNAME} \
--overview-name=${MAPNAME} \
--generate-sea=multipolygon,extend-sea-sectors,close-gaps=6000 \
--net \
--gmapsupp \
--tdbfile \
--remove-short-arcs \
--index \
--route \
--add-pois-to-areas \
--road-name-pois=0x640a \
--draw-priority=50 \
--latin1 \
--make-opposite-cycleways \
--make-cycleways \
-c ${TOOL_DIR}/template.args ${TYP_DIR}/${TYPFILE}"
echo "Executing ${CMD}"
eval ${CMD}
mv ${TOOL_DIR}/gmapsupp.img ${TOOL_DIR}/base.img
mv osmmap.tdb basemap.tdb
mv osmmap.img basemap.img
mv template.args template_base.args
mv areas.list areas_base.list

# check if contourlines should be created at all
if [[ "${NOCONTOURS}" != "YES" ]]
then
   # first check if *.img for contourdata already exist. If yes, 
   # do not create any contourdata
   if [[ ! -e ${SRTMMINMAPNAME}.img ||  ! -e ${SRTMMAJMAPNAME}.img ]]
   then
      echo "creating contourdata now ..."
      # now check if file with contourdata already exists 
      if [[ -z "${CONTOURS}" || ! -e ${CONTOURS} ]]
      then
         CONTOURS=${TOOL_DIR}/srtm.osm
         echo "retrieving contour data ..."
         mono ${TOOL_DIR}/Srtm2Osm/Srtm2Osm.exe -bounds1 ${BOTTOM} ${LEFT} ${TOP} \
         ${RIGHT} -step ${CSTEPMIN} -cat ${CSTEPMAX} ${CSTEPMED} -large \
         -corrxy 0.000 0.0005 -o ${CONTOURS}
      else
         echo "using existing file ${CONTOURS}"
      fi

      echo "splitting contourfile ..."
      CMD=" java -Xmx2000M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar
      --mapid=${SRTMMINID}0001 \
      --mixed --cache=${TOOL_DIR}/${SPLITTER_DIR}/cache/ --max-nodes=5000000 \
      --max-areas=20 ${CONTOURS}"
      echo "Executing $CMD"
      eval $CMD
      cp template.args template_srtm10.args
      cp template.args template_srtm20.args

      echo "editing template files ..."
      sed -e "s/# description: OSM Map/description: SRTMMIN/"\
         template_srtm10.args > template_${SRTMMINMAPNAME}.args
      sed -e "s/mapname: ${SRTMMINID}/mapname: ${SRTMMAJID}/; s/# description: OSM Map/description: SRTMMAJ/"\
         template_srtm20.args > template_${SRTMMAJMAPNAME}.args 

      echo "creating image file for contourlines (minor) ..."
      CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
      --style-file=${STYLES_DIR}/mkgmap-style-srtm10new/ \
      --net \
      --gmapsupp \
      --tdbfile \
      --family-id=${SRTMFAMMIN} \
      --product-id=1 \
      --draw-priority=28 \
      --transparent \
      --series-name=${SRTMMINMAPNAME} \
      --family-name=${SRTMMINMAPNAME} \
      --area-name=Germany \
      -c ${TOOL_DIR}/template_${SRTMMINMAPNAME}.args ${TYP_DIR}/${SRTMMINTYP}"
      echo "Executing $CMD"
      eval $CMD
      mv ${TOOL_DIR}/gmapsupp.img ${TOOL_DIR}/${SRTMMINMAPNAME}.img
      mv osmmap.tdb srtm10map.tdb
      mv osmmap.img srtm10map.img

      echo "creating image file for contourlines (medium / major) ..."
      CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
      --style-file=${STYLES_DIR}/mkgmap-style-srtm20new/ \
      --net \
      --gmapsupp \
      --tdbfile \
      --family-id=${SRTMFAMMAJ} \
      --product-id=1 \
      --draw-priority=28 \
      --transparent \
      --series-name=${SRTMMAJMAPNAME} \
      --family-name=${SRTMMAJMAPNAME} \
      --area-name=Germany \
      -c ${TOOL_DIR}/template_${SRTMMAJMAPNAME}.args ${TYP_DIR}/${SRTMMAJTYP}"
      echo "Executing $CMD"
      eval $CMD
      mv ${TOOL_DIR}/gmapsupp.img ${TOOL_DIR}/${SRTMMAJMAPNAME}.img
      mv osmmap.tdb srtm20map.tdb
      mv osmmap.img srtm20map.img
   else
      echo "${SRTMMINMAPNAME}.img and ${SRTMMAJMAPNAME}.img already exist, won't create them again!"
   fi

   # remove intermediate files
   rm *.gz
   echo "combining *.img files into final mapfile ..."
   ${TOOL_DIR}/gmaptool/gmt -j -o ${TOOL_DIR}/${MAPNAME}.img -m "OSM" ${TOOL_DIR}/base.img \
   ${TOOL_DIR}/${SRTMMINMAPNAME}.img ${TOOL_DIR}/${SRTMMAJMAPNAME}.img
else
   # no contourlines, just rename basemap file to desired name
   echo "no contourlines will be created ..."
   rm *.gz
   mv ${TOOL_DIR}/base.img ${TOOL_DIR}/${MAPNAME}.img 
fi

