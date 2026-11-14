#!/usr/bin/env bash
# Downloads the public data used to build the two maps, into ./map-data
# (git-ignored). Then rebuild with:
#   python3 scripts/area_map.py map-data _data/business.yml _includes/area-map.html
#   python3 scripts/contours.py map-data assets/img/harris-contours.svg
# Sources: U.S. Census TIGERweb (boundaries, water, highways) and AWS Terrain
# Tiles (elevation; USGS NED / SRTM). All public domain.
# To add a town to the area map: add it to _data/business.yml, add its Census
# place name to the queries below (or a lat/lon in area_map.py if it isn't a
# Census place), re-run this script and area_map.py, and add a LABEL offset.
set -euo pipefail
D=map-data; mkdir -p "$D/tiles"
T=https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb
ENV='-95.32,29.58,-94.80,30.10'
get() { curl -sf -G "$1" "${@:3}" --data-urlencode "outSR=4326" --data-urlencode "f=geojson" -o "$D/$2"; }
get "$T/Places_CouSub_ConCity_SubMCD/MapServer/4/query" incorporated.geojson \
  --data-urlencode "where=STATE='48' AND BASENAME IN ('Baytown','Deer Park','La Porte','Pasadena','Mont Belvieu')" \
  --data-urlencode "outFields=BASENAME,NAME,GEOID,INTPTLAT,INTPTLON" --data-urlencode "maxAllowableOffset=0.0004"
get "$T/Places_CouSub_ConCity_SubMCD/MapServer/5/query" cdp.geojson \
  --data-urlencode "where=STATE='48' AND BASENAME IN ('Channelview','Highlands','Crosby')" \
  --data-urlencode "outFields=BASENAME,NAME,GEOID,INTPTLAT,INTPTLON" --data-urlencode "maxAllowableOffset=0.0004"
get "$T/State_County/MapServer/1/query" counties.geojson \
  --data-urlencode "where=GEOID IN ('48201','48071','48291','48339','48167','48039','48157')" \
  --data-urlencode "outFields=NAME,GEOID" --data-urlencode "maxAllowableOffset=0.0006"
get "$T/State_County/MapServer/1/query" harris.geojson \
  --data-urlencode "where=GEOID='48201'" --data-urlencode "outFields=NAME,GEOID"
for spec in "Hydro/MapServer/1|water.geojson|AREAWATER > 1500000|NAME,MTFCC,AREAWATER|0.0006" \
            "Transportation/MapServer/2|primary.geojson|1=1|NAME,MTFCC,RTTYP|0.0008" \
            "Transportation/MapServer/3|secondary.geojson|RTTYP IN ('U','I')|NAME,MTFCC,RTTYP|0.0008"; do
  IFS='|' read -r layer out where fields off <<< "$spec"
  get "$T/$layer/query" "$out" --data-urlencode "where=$where" --data-urlencode "geometry=$ENV" \
    --data-urlencode "geometryType=esriGeometryEnvelope" --data-urlencode "inSR=4326" \
    --data-urlencode "spatialRel=esriSpatialRelIntersects" --data-urlencode "outFields=$fields" \
    --data-urlencode "maxAllowableOffset=$off"
done
# Elevation tiles (zoom 11) covering Harris County, for the contour map
for x in $(seq 478 484); do for y in $(seq 843 848); do
  curl -sf -o "$D/tiles/11-$x-$y.png" "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/11/$x/$y.png"
done; done
echo "done: $(ls "$D" | wc -l) files"
