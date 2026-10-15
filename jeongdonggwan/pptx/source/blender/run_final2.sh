#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN JD_VARIANT
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
runv() { n=$1; var=$2; view=$3; shift 3; env JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene.py -- $view "$OUTW/alt_${n}.png" 160 1920 > "alt_${n}.log" 2>&1; echo "done alt $n $(date +%H:%M:%S)"; }
runm() { v=$1; shift; env "$@" timeout 1500 $B -b --python build_scene.py -- $v "$OUTW/f_${v}.png" 192 1920 > "f2_${v}.log" 2>&1; echo "done main $v $(date +%H:%M:%S)"; }
runv saintluc saintluc hero_sw JD_EXPO=-0.1
runv lincoln lincoln hero_sw JD_EXPO=-0.1
runv blaibach blaibach hero_sw JD_DUSK=1 JD_EXPO=0.0
runv saintluc_b saintluc roof_view JD_EXPO=-0.1
runv lincoln_b lincoln street_nw JD_EXPO=-0.1
runv blaibach_b blaibach street_nw JD_DUSK=1 JD_EXPO=0.0
runm hero_sw JD_EXPO=0.0
runm night_sw JD_EXPO=0.3
runm street_nw JD_EXPO=0.0
runm sunken JD_EXPO=0.5
runm lane_entry JD_EXPO=-0.4
runm aerial JD_EXPO=0.0
echo ALLDONE
