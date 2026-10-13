#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN JD_VARIANT JD_MASSING
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
run() { n=$1; mj=$2; var=$3; view=$4; shift 4; env JD_MASSING="$(cygpath -m "$TEMP/bl/massing_${mj}.json")" JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene2.py -- $view "$OUTW/form_${n}.png" 160 1920 > "form_${n}.log" 2>&1; echo "done $n $(date +%H:%M:%S)"; }
run C_aerial C blaibach aerial JD_EXPO=0.0
run C_hero C blaibach hero_sw JD_DUSK=1 JD_EXPO=0.0
echo ALLDONE
