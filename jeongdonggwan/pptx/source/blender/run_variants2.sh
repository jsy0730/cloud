#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl"
OUTW=$(cygpath -w "$TEMP/bl/out")
B=blender/blender-5.2.2-windows-x64/blender.exe
run() { n=$1; var=$2; view=$3; shift 3; env JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene.py -- $view "$OUTW\w_$n.png" 160 1920 > "w_$n.log" 2>&1; echo "done $n $(date +%H:%M:%S)"; }
run green_a green hero_sw JD_EXPO=-0.1
run kinetic_a kinetic hero_sw JD_DUSK=1 JD_EXPO=0.0
run lantern_a lantern hero_sw JD_NIGHT=1 JD_EXPO=0.9
run kinetic_b kinetic street_nw JD_DUSK=1 JD_EXPO=0.0
run green_b green street_nw JD_EXPO=-0.1
run lantern_b lantern street_nw JD_NIGHT=1 JD_EXPO=0.9
echo ALLDONE
