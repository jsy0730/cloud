#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1 JD_VIEWS="$(cygpath -m "$TEMP/bl/views_v3.json")"
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN JD_VARIANT JD_MASSING
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
runv() { n=$1; var=$2; view=$3; shift 3; env JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene4.py -- $view "$OUTW/alt4_${n}.png" 160 1920 > "alt4_${n}.log" 2>&1; echo "done alt $n $(date +%H:%M:%S)"; }
runm() { n=$1; mj=$2; var=$3; view=$4; shift 4; env JD_MASSING="$(cygpath -m "$TEMP/bl/massing_${mj}.json")" JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene4.py -- $view "$OUTW/form4_${n}.png" 160 1920 > "form4_${n}.log" 2>&1; echo "done form $n $(date +%H:%M:%S)"; }
runv saintluc saintluc hero_sw JD_EXPO=-0.1
runv lincoln lincoln hero_sw JD_EXPO=-0.1
runv blaibach blaibach hero_sw JD_DUSK=1 JD_EXPO=0.0
runm A_aerial A saintluc aerial JD_EXPO=0.0
runm B_aerial B lincoln aerial JD_EXPO=0.0
runm C_aerial C blaibach aerial JD_EXPO=0.0
echo ALLDONE
