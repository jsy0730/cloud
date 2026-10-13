import os
p = os.path.join(os.environ['TEMP'], 'work', 'build_ds.js')
s = open(p, encoding='utf8').read()
cnt = 0


def rep(a, b):
    global s, cnt
    if a not in s:
        print('MISSING:', a[:60]); return
    s = s.replace(a, b); cnt += 1


rep("차가 멈추는 주차층은 차분한 전돌 스크린으로 감싸고, 사람이 움직이는 순환 계단 · 6F 가변홀 · 옥상 광장은 붉은 계단과 켜진 홀로 드러냄",
    "차가 멈추는 주차층은 목재 슬랫 스크린으로 차분히 감싸고, 사람이 움직이는 순환 계단 · 6F 가변홀 · 옥상 광장은 검은 계단과 켜진 홀로 드러냄")
rep("주차층 전돌 스크린 · 붉은 순환 계단", "주차층 목재 슬랫 스크린 · 검은 순환 계단")
rep("停은 전돌 스크린으로 조용하게, 動은 붉은 순환 계단으로 눈에 띄게 드러냄", "停은 목재 슬랫 스크린으로 차분하게, 動은 검은 순환 계단과 켜진 홀로 드러냄")
rep("apply: '두 끝을 비워 지하 공연장까지 빛을 내림'", "apply: '주차층 외피를 목재 슬랫 스크린으로 구성, 두 끝을 비워 지하 공연장까지 빛을 내림'")
rep("서측 면은 타공 전돌 스크린", "서측 면은 목재 슬랫 스크린")
rep("'투시도: 개념 볼륨 모델 + OpenStreetMap 높이 자료(주변 건물 단순화) · 실제 설계안이 아님, 조명 계획 · 광장 시설 배치는 개념'",
    "'투시도: 개념 볼륨 모델(Blender Cycles 렌더) + OpenStreetMap 높이 자료(주변 건물 단순화) · 실제 설계안이 아님, 재질 · 조명 · 광장 시설 배치는 개념'")
open(p, 'w', encoding='utf8').write(s)
print('replaced', cnt)
import re
left = [m.group(0) for m in re.finditer(r'.{12}(전돌|붉은).{12}', s)]
print('remaining:', left)
