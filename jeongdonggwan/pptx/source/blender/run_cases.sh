#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
S=${1:-64}; RX=${2:-960}; PFX=${3:-c}
run() { n=$1; var=$2; view=$3; shift 3; env JD_VARIANT=$var "$@" timeout 1500 $B -b --python build_scene.py -- $view "$OUTW/${PFX}_${n}.png" $S $RX > "${PFX}_${n}.log" 2>&1; echo "done $n $(date +%H:%M:%S)"; }
run saintluc saintluc hero_sw JD_EXPO=-0.1
run lincoln lincoln hero_sw JD_EXPO=-0.1
run blaibach blaibach hero_sw JD_DUSK=1 JD_EXPO=0.0
echo ALLDONE
