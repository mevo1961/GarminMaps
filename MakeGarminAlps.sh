#!/bin/bash


# Startmeldung geben und Parameter / Optionen prüfen
echo $$: $0 "$*"
while getopts ":i:o:w:" OPT
do
   case $OPT in
   i ) INFILE=$OPTARG ;;
   o ) CONTOURS_O=$OPTARG ;;
   w ) CONTOURS_W=$OPTARG ;;
   * ) echo "Invalid Option" ;;
   esac
done
if [[ -f $INFILE ]] 
then
   echo "OSM file: ${INFILE}"
else
   echo "you must specify an OSM file for the basemaps!"
   exit 1
fi


# set some required variables
TOOL_DIR=$(pwd)
MKGMAP_DIR=$(ls | grep mkgmap)
SPLITTER_DIR=$(ls | grep splitter)
LEFT=8.9
RIGHT=15.9
BOTTOM=45.5
TOP=48.3
MAPID=3100
SRTMID=2300
FAMID=1305
TYPFILE=${FAMID}.TYP
MAPNAME=OSM_Ostalpen

# cut selected area from input file
echo "Cutting $MAPNAME from ${INFILE}: Left=${LEFT}, Right=${RIGHT},"
echo "Bottom=${BOTTOM}, Top=${TOP}"
${TOOL_DIR}/osmosis*/bin/osmosis --read-xml enableDateParsing=no \
${INFILE} --bounding-box left=${LEFT} right=${RIGHT} bottom=${BOTTOM}  \
top=${TOP} completeWays=no --write-xml file=${TOOL_DIR}/temp.osm

echo "splitting area into tiles ..."
java -Xmx1024M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar \
--mapid=${MAPID}0001 --max-nodes=800000 ${TOOL_DIR}/temp.osm

rm temp.osm

echo "creating basemap $MAPNAME..."
echo "Using Mapid=${MAPID}, FamilyID=${FAMID}, Typfile=${TYPFILE}"
CMD="java -Xmx1024M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
--description=OSM_OALPS \
--country-name=Germany \
--country-abbr=DE \
--name-tag-list="name:de,name,int_name" \
--style-file=${TOOL_DIR}/${MKGMAP_DIR}/mkgmap-style-toponew/ \
--family-id=${FAMID} \
--product-id=1 \
--series-name=${MAPNAME} \
--family-name=${MAPNAME} \
--area-name=Alps \
--overview-name=${MAPNAME} \
--net \
--gmapsupp \
--tdbfile \
--remove-short-arcs \
--route \
--road-name-pois=0x640a \
--draw-priority=25 \
--latin1 \
--make-opposite-cycleways \
-c ${TOOL_DIR}/template.args ${TOOL_DIR}/${TYPFILE}"
echo "Executing ${CMD}"
eval ${CMD}
mv gmapsupp.img osm_o.img
mv osmmap.tdb ostalpen.tdb
mv osmmap.img ostalpen.img

rm ${MAPID}*.gz

if [[ -z ${CONTOURS_O} || ! -f ${CONTOURS_O} ]]
then
   CONTOURS_O=${TOOL_DIR}/srtm.osm
   echo "retrieving contour data ..."
   mono ${TOOL_DIR}/Srtm2Osm/Srtm2Osm.exe -bounds1 ${BOTTOM} ${LEFT} ${TOP} \
   ${RIGHT} -step 25 -cat 400 100 -large -corrxy 0.000 0.0005 \
   -o ${CONTOURS_O}
else
   echo "using existing file ${CONTOURS_O}"
fi

echo "splitting contourfile ..."
CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar \
--mapid=${SRTMID}0001 --mixed=yes --cache=${TOOL_DIR}/${SPLITTER_DIR}/cache/ \
--max-nodes=5000000 --max-areas=27 ${CONTOURS_O}"
echo "Executing $CMD"
eval $CMD

echo "editing template file ..."
sed -e 's/# description: OSM Map/description: SRTM25_O/'\
        template.args > template_srtm25_o.args

echo "creating image file for contourlines  ..."
CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
--style-file=${TOOL_DIR}/${MKGMAP_DIR}/mkgmap-style-srtm25new/ \
--net \
--gmapsupp \
--tdbfile \
--family-id=${SRTMID} \
--product-id=1 \
--draw-priority=30 \
--transparent \
--series-name=SRTM25_O \
--family-name=SRTM25_O \
--area-name=Alps \
-c ${TOOL_DIR}/template_srtm25_o.args"
echo "Executing $CMD"
eval $CMD
mv ${TOOL_DIR}/gmapsupp.img ${TOOL_DIR}/srtm25_o.img
mv osmmap.tdb srtm25omap.tdb
mv osmmap.img srtm25omap.img

rm ${SRTMIS}*.gz
echo "combining *.img files into final mapfile ..."
${TOOL_DIR}/gmaptool/gmt -j -o ${TOOL_DIR}/${MAPNAME}.img ${TOOL_DIR}/osm_o.img \
${TOOL_DIR}/srtm25_o.img

# now do the same for the western alps
LEFT=5.0
RIGHT=8.9
BOTTOM=43.5
TOP=48.3
MAPID=3200
SRTMID=2400
FAMID=1337
TYPFILE=${FAMID}.TYP
MAPNAME=OSM_Westalpen

# cut selected area from input file
echo "Cutting ${MAPNAME} from ${INFILE}: Left=${LEFT}, Right=${RIGHT},"
echo "Bottom=${BOTTOM}, Top=${TOP}"
${TOOL_DIR}/osmosis*/bin/osmosis --read-xml enableDateParsing=no \
${INFILE} --bounding-box left=${LEFT} right=${RIGHT} bottom=${BOTTOM}  \
top=${TOP} completeWays=no --write-xml file=${TOOL_DIR}/temp.osm

echo "splitting area into tiles ..."
java -Xmx1024M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar \
--mapid=${MAPID}0001 --max-nodes=800000 ${TOOL_DIR}/temp.osm

rm temp.osm

echo "creating basemap ${MAPNAME}..."
echo "Using Mapid=${MAPID}, FamilyID=${FAMID}, Typfile=${TYPFILE}"
CMD="java -Xmx1024M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
--description=OSM_WALPS \
--country-name=Germany \
--country-abbr=DE \
--name-tag-list="name:de,name,int_name" \
--style-file=${TOOL_DIR}/${MKGMAP_DIR}/mkgmap-style-toponew/ \
--family-id=${FAMID} \
--product-id=1 \
--series-name=${MAPNAME} \
--family-name=${MAPNAME} \
--area-name=Alps \
--overview-name=${MAPNAME} \
--net \
--gmapsupp \
--tdbfile \
--remove-short-arcs \
--route \
--road-name-pois=0x640a \
--draw-priority=25 \
--latin1 \
--make-opposite-cycleways \
-c ${TOOL_DIR}/template.args ${TOOL_DIR}/${TYPFILE}"
echo "Executing ${CMD}"
eval ${CMD}
mv gmapsupp.img osm_w.img
mv osmmap.tdb westalpen.tdb
mv osmmap.img westalpen.img

rm ${MAPID}*.gz

if [[ -z ${CONTOURS_W} || ! -f ${CONTOURS_W} ]]
then
   CONTOURS_W=${TOOL_DIR}/srtm.osm
   echo "retrieving contour data ..."
   mono ${TOOL_DIR}/Srtm2Osm/Srtm2Osm.exe -bounds1 ${BOTTOM} ${LEFT} ${TOP} \
   ${RIGHT} -step 25 -cat 400 100 -large -corrxy 0.000 0.0005 \
   -o ${CONTOURS_W}
else
   echo "using existing file ${CONTOURS_W}"
fi

echo "splitting contourfile ..."
CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${SPLITTER_DIR}/splitter.jar \
--mapid=${SRTMID}0001 --mixed=yes --cache=${TOOL_DIR}/${SPLITTER_DIR}/cache/ \
--max-nodes=5000000 --max-areas=27 ${CONTOURS_W}"
echo "Executing $CMD"
eval $CMD

echo "editing template file ..."
sed -e 's/# description: OSM Map/description: SRTM25_W/'\
        template.args > template_srtm25_w.args

echo "creating image file for contourlines  ..."
CMD=" java -Xmx1536M -jar ${TOOL_DIR}/${MKGMAP_DIR}/mkgmap.jar \
--style-file=${TOOL_DIR}/${MKGMAP_DIR}/mkgmap-style-srtm25new/ \
--net \
--gmapsupp \
--tdbfile \
--family-id=${SRTMID} \
--product-id=1 \
--draw-priority=30 \
--transparent \
--series-name=SRTM25_W \
--family-name=SRTM25_W \
--area-name=Alps \
-c ${TOOL_DIR}/template_srtm25_w.args"
echo "Executing $CMD"
eval $CMD
mv ${TOOL_DIR}/gmapsupp.img ${TOOL_DIR}/srtm25_w.img
mv osmmap.tdb srtm25wmap.tdb
mv osmmap.img srtm25wmap.img

rm ${MAPID}*.gz
echo "combining *.img files into final mapfile ..."
${TOOL_DIR}/gmaptool/gmt -j -o ${TOOL_DIR}/${MAPNAME}.img \
${TOOL_DIR}/osm_w.img ${TOOL_DIR}/srtm25_w.img
