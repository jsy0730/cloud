#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl"
OUTW=$(cygpath -w "$TEMP/bl/out")
for v in lane_entry sunken hero_sw night_sw street_nw roof_view aerial; do
  EX=""; [ "$v" = "sunken" ] && EX="0.5"
  JD_EXPO="${EX:-$( [ "$v" = night_sw ] && echo 0.3 || ( [ "$v" = lane_entry ] && echo -0.4 || echo 0.0 ) )}" timeout 1500 blender/blender-5.2.2-windows-x64/blender.exe -b --python build_scene.py -- $v "$OUTW\f_$v.png" 192 1920 > "f_$v.log" 2>&1
  echo "done $v $(date +%H:%M:%S)"
done
echo ALLDONE
