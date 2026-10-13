#!/bin/bash
# usage: run_v3.sh <view> <name> <samples> <res> [ENV=val ...]
cd "$TEMP/bl"
export JD_ROOT="$TEMP/cloud_repo/jeongdonggwan/build/render" JD_PH="$TEMP/bl/ph" JD_FILL="$TEMP/bl" JD_NOPEOPLE=1 JD_VIEWS="$(cygpath -m "$TEMP/bl/views_v3.json")"
unset JD_RAYCAST JD_HIDE JD_DUSK JD_NIGHT JD_TOPDOWN JD_VARIANT JD_MASSING
OUTW="$(cygpath -m "$TEMP/bl/out")"
B=blender/blender-5.2.2-windows-x64/blender.exe
VIEW=$1; NAME=$2; SAMP=$3; RES=$4; shift 4
env JD_EXPO=0.0 "$@" timeout 3000 $B -b --python build_scene3.py -- $VIEW "$OUTW/${NAME}.png" $SAMP $RES > "${NAME}.log" 2>&1
echo "done $NAME $(date +%H:%M:%S)"
