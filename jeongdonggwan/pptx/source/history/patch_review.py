import re, os
p = 'build_ds.js'
s = open(p, encoding='utf8').read()
n = 0
def rep(a, b, all_=False):
    global s, n
    if a not in s:
        print('MISSING:', a[:70]); return
    s = s.replace(a, b) if all_ else s.replace(a, b, 1); n += 1

# numbers / wording
rep("한 층 약 4,232㎡의 정형 바닥", "한 층 4,322.1㎡의 정형 바닥")
rep("정동관 그림자 · 동지 09·12·15시, 높이 29.8m 기준 (붉은 선 = 대지, 점선 = 제3종일반주거 경계 약 45m)",
    "정동관 그림자 · 동지 09·12·15시, 지붕 설비 포함 높이 29.8m 기준 (붉은 선 = 대지, 점선 = 제3종일반주거 경계 약 45m)")
rep("'홀(29.8m)이 광장의 북쪽에 있음'", "'홀(29.1m, 지붕 설비 포함 29.8m)이 광장의 북쪽에 있음'")
rep("takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽으로 분리함'", "takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽 중심으로 분리함(소로 횡단 1곳)'")
rep("'동측 주거 쪽 차량 진출입 없음'], wrap: 1 }] }], { size: 10 });\n  takeaway", "'주 진출입은 남·북단 소로만 사용'], wrap: 1 }] }], { size: 10 });\n  takeaway")
rep("'동측 주거 쪽 차량 진출입 없음'] }] }], { size: 10 });", "'동측 주거 쪽 주 차량 진출입 없음'] }] }], { size: 10 });")
rep("두 역 도보권과 카페거리 사이, 공영주차장이 비어 있는 곳임", "두 역 도보권과 카페거리 사이, 반경 내 공영주차장이 거의 없는 곳임")
rep("'이번 판에서 다루지 않은 것'", "'본 보고서에서 다루지 않은 사항'")
rep("'본 시안 · 정동관 내용 문서의 열린 이슈와 같은 항목 · 수치는 모두 개략이며 확정은 법규 원문 확인과 작도에서 이뤄짐'", "'본 시안의 열린 이슈 · 수치는 모두 개략이며 확정은 법규 원문 확인과 작도에서 이뤄짐'")
rep("투시도 외 도면(평면 · 단면 상세)", "상세 평면 · 단면(미작성)")
rep("팀 조사(2026.9) · 다이어그램은 팀 작성", "자체 조사(2026.9) · 다이어그램은 자체 작성 · 평택 JS타워 사진은 출처 미확인(저장소 자료)")
rep("팀 조사(2026.9)');\n  caseCol(s, M, 1.0, { name: 'Saint-Luc", "자체 조사(2026.9)');\n  caseCol(s, M, 1.0, { name: 'Saint-Luc")
s = s.replace("팀 조사(2026.9)", "자체 조사(2026.9)")
rep("'타공판 밴드가 일사와 주차층 시선을 함께 가림(사진에서 읽은 내용)'", "'타공판 밴드가 일사와 주차층 시선을 함께 가림'")
rep("Herzog & de Meuron(1111 Lincoln Road, 사진 Phillip Pessar, CC BY 2.0), 자체 조사(2026.9)", "Herzog & de Meuron(1111 Lincoln Road, 사진 Phillip Pessar, CC BY 2.0 · 삽입 사진 ArchDaily), 자체 조사(2026.9)")
# sources on slide 3
rep("'파이낸셜뉴스(2022.07.11), 부산일보(2024.07.04), 글로벌경제(2021), 전국주차장정보표준데이터, 토지이음(2026.10.11) · 69.1%는 주차환경개선지구 67곳 평균'",
    "'파이낸셜뉴스(2022.07.11), 부산일보(2024.07.04), 부산진구 수급실태조사(2023), 글로벌경제(2021), 전국주차장정보표준데이터(2026.04), 토지이음(2026.10.11) · 69.1%는 주차환경개선지구 67곳 평균'")
rep("cap(s, '확보율 기준선 130% · 부산진구는 등록 대비 118.5%', M, 3.68, 4.95);", "cap(s, '기준 130% · 부산 전체는 2021년, 부산진구는 등록 대비 2023년 값', M, 3.68, 4.95);")
# noise
rep("cap(s, '주간 소음 분포 추정 · 가정 교통량, 건물 차폐 미반영', M, 1.0 + hm + 0.02, wm);", "cap(s, '● = 면별 평가점(북·서·남·동·주거 경계)', M, 1.0 + hm + 0.02, wm);")
rep("valAxisHidden: true, valAxisMinVal: 40, valAxisMaxVal: 80, valGridLine: { style: 'none' }", "valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 90, valGridLine: { style: 'none' }")
# donut note
rep("'주차장', '75.62% · 32,988.4㎡', D1]", "'주차장', '75.62% · 32,988.4㎡', D1]") if False else None
rep("noteBox(s, x2, 6.35, w2, 0.45, null, '주차 비율 75.62%(요건 70% 이상), 주차는 약 600대로 표기', { size: 9.5 });",
    "noteBox(s, x2, 6.2, w2, 0.62, null, '주차장 32,988.4㎡에는 1F 램프 · 정산 · 이륜차 1,200㎡가 포함됨. 주차 비율 75.62%(요건 70% 이상)', { size: 9.5 });")
# render subtitle + tags
rep("'옥상 광장 · 선큰 마당 · 소로'", "'옥상 광장 · 끝 코어 · 소로'")
rep("""  const tag_ = (label, x, y) => s.addText(label, { x, y, w: Math.min(6.2, label.length * 0.118 + 0.35), h: 0.27, fontFace: F, fontSize: 9.5, bold: true, color: INK, fill: { color: 'FFFFFF' }, margin: [0, 6, 0, 6], valign: 'middle', isTextBox: true });""",
    """  const tag_ = (label, x, y) => s.addText(label, { x, y, w: Math.min(6.2, label.length * 0.125 + 0.4), h: 0.28, fontFace: F, fontSize: 9.5, bold: true, color: 'FFFFFF', fill: { color: NAVY }, margin: 0, align: 'center', valign: 'middle', isTextBox: true });""")
# sections: remove duplicate captions
rep("  cap(s, 'A 종단면 · 소로를 따라 펼친 개념 단면 (남 → 북)', M, 1.0 + ha + 0.03, wa);\n", "")
rep("  cap(s, 'B 횡단면 (y=70m)', 9.2, 1.0 + hb + 0.03, 2.45);\n", "")
# cover disclaimer contrast
rep("T(s, '투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님', SW - 6.0, 7.18, 5.6, 0.22, { fontSize: 8, color: 'FFFFFF', align: 'right' });",
    "R(s, SW - 6.15, 7.13, 6.15, 0.37, '101216');\n  T(s, '투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님', SW - 6.0, 7.13, 5.8, 0.37, { fontSize: 9, color: 'FFFFFF', align: 'right', valign: 'middle' });")
# concept slide page number
rep("  T(s, '停動館', M, 7.0, 1.1, 0.4, { fontFace: SERIF, bold: true, fontSize: 16, color: NAVY, valign: 'middle' });\n}", "  T(s, '停動館', M, 7.0, 1.1, 0.4, { fontFace: SERIF, bold: true, fontSize: 16, color: NAVY, valign: 'middle' });\n  T(s, '담당자 정성윤 · ' + String(PAGE).padStart(2, '0'), 3.9, 7.06, 4.6, 0.3, { fontSize: 8, color: MUTED, align: 'right' });\n}")
# footers a bit larger
rep("T(s, '출처: ' + source, 1.65, 7.06, 9.6, 0.34, { fontSize: 8, color: MUTED, valign: 'top' });", "T(s, '출처: ' + source, 1.65, 7.06, 9.55, 0.4, { fontSize: 8.5, color: MUTED, valign: 'top' });")
# keep Korean words intact: post-process step appended to writeFile
rep("pres.writeFile({ fileName: path.join(__dirname, 'jeongdonggwan_gs.pptx') }).then((f) => console.log('wrote', f));",
    "pres.writeFile({ fileName: path.join(__dirname, 'jeongdonggwan_gs.pptx') }).then((f) => { require('child_process').execFileSync('python', ['-I', path.join(__dirname, 'nobreak.py'), f], { stdio: 'inherit' }); console.log('wrote', f); });")
open(p, 'w', encoding='utf8').write(s)
print('replacements', n)
