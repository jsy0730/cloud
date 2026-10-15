#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph"
OUTW=$(cygpath -w "$TEMP/bl/out")
for v in hero_sw night_sw street_nw roof_view sunken lane_entry aerial; do
  timeout 400 blender/blender-5.2.2-windows-x64/blender.exe -b --python build_scene.py -- $v "$OUTW\q_$v.png" 40 800 > "q_$v.log" 2>&1
  echo "done $v"
done
