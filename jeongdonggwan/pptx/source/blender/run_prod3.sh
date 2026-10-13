#!/bin/bash
cd "$TEMP/bl"
./run_v3.sh hero_sw f3_hero_sw 192 1920 JD_EXPO=0.0
./run_v3.sh stair_close f3_stair_close 192 1920 JD_EXPO=0.0
./run_v3.sh night_sw f3_night_sw 192 1920 JD_EXPO=0.3
./run_v3.sh street_nw f3_street_nw 192 1920 JD_EXPO=0.0
./run_v3.sh roof_view f3_roof_view 192 1920 JD_EXPO=0.0
./run_v3.sh lane_entry f3_lane_entry 192 1920 JD_EXPO=-0.4
./run_v3.sh aerial f3_aerial 192 1920 JD_EXPO=0.0
./run_v3.sh sunken f3_sunken 192 1920 JD_EXPO=0.5
echo ALLDONE
