#!/bin/bash
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN JD_VARIANT JD_MASSING
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
SAMP=${1:-48}; RES=${2:-960}; NAME=${3:-h3_test}
env JD_EXPO=0.0 timeout 3000 $B -b --python build_scene3.py -- hero_sw "$OUTW/${NAME}.png" $SAMP $RES > "${NAME}.log" 2>&1
echo "done $NAME $(date +%H:%M:%S)"
