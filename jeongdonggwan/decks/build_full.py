# -*- coding: utf-8 -*-
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import *
D = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/decks/'
lib.ASSET.update(json.load(open(D + 'assets.json'))['A'])
OUT = D + 'full/project/slides/'; os.makedirs(OUT, exist_ok=True)
SL = []   # (id, html)
def add(sid, h): SL.append((sid, h)); open(OUT + sid + '.html', 'w').write(h)
pg = lambda: f'{len(SL) + 1:02d}'
AR = json.load(open(D + '../build/areas.json'))

def donut(vals, cols, size=330, r_out=150, r_in=88):
    tot = sum(vals); a0 = -math.pi / 2; paths = []; cx = cy = size / 2
    for v, c in zip(vals, cols):
        a1 = a0 + v / tot * 2 * math.pi; large = 1 if a1 - a0 > math.pi else 0
        p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
        x1, y1 = p(r_out, a0); x2, y2 = p(r_out, a1); x3, y3 = p(r_in, a1); x4, y4 = p(r_in, a0)
        paths.append(f'<path d="M{x1:.1f} {y1:.1f} A{r_out} {r_out} 0 {large} 1 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} A{r_in} {r_in} 0 {large} 0 {x4:.1f} {y4:.1f} Z" fill="{c}" stroke="#ffffff" stroke-width="2"/>')
        a0 = a1
    return f'<svg aria-label="연면적 용도별 구성비 도넛 차트: 주차장 75.62%, 문화·공연 11.58%, 상업·상인 5.96%, 코어 3.44%, 설비·지원 3.40%" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + ''.join(paths) + '</svg>'

# ---------------------------------------------------------------- 01 cover
add('cover', f'''<section id="cover" style="background:#141414;color:#ffffff;{REG}padding:0px">
<img src="{blob('hero')}" alt="전포대로에서 본 정동관 주간 투시도, 전돌 스크린 주차층과 붉은 순환 계단" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover">
<div style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;background:linear-gradient(90deg, rgba(8,12,24,0.88), rgba(8,12,24,0.55) 45%, rgba(8,12,24,0.0) 80%)"></div>
<p style="position:absolute;left:96px;top:84px;width:900px;{BOLD}font-size:40px;line-height:1.3;color:#ffffff">2026 · 공학설계기초</p>
<p style="position:absolute;left:96px;top:190px;width:1300px;{SERIF}font-size:250px;line-height:1.05;letter-spacing:6px;white-space:nowrap;color:#ffffff">停動館</p>
<p style="position:absolute;left:96px;top:560px;width:1200px;{XB}font-size:110px;line-height:1.1;letter-spacing:-2px;color:#ffffff">전포 정동관</p>
<p style="position:absolute;left:96px;top:700px;width:1300px;{BOLD}font-size:48px;line-height:1.3;color:#ffc000">낮에는 주차장, 밤에는 공연과 옥상 광장</p>
<p style="position:absolute;left:96px;top:790px;width:1300px;font-size:32px;line-height:1.5;color:#ffffff">복합주차장 시안 · 부산진구 전포동 207번지 일대 53필지 4,964.5㎡<br>지하 4층 · 지상 6층 + 옥상 · 연면적 43,623.7㎡ · 주차 약 600대</p>
<p style="position:absolute;left:96px;top:960px;width:700px;{BOLD}font-size:36px;line-height:1.3;color:#ffffff">202325137 정성윤</p>
<p style="position:absolute;left:96px;top:1020px;width:1500px;font-size:24px;line-height:1.3;color:#d9d9d9">투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님</p>
</section>
''')

# ---------------------------------------------------------------- 02 contents
def cn(n, name, lines, on=True):
    ls = ''.join(f'<p style="font-size:30px;line-height:1.5">- {l}</p>' for l in lines)
    return (f'<div style="display:flex;flex-direction:row;gap:30px;align-items:flex-start;width:1180px">'
            f'<p style="{XB}font-size:96px;line-height:1;width:170px;flex:none;color:#ffffff;-webkit-text-stroke:3px {NAVY}">{n}</p>'
            f'<div style="display:flex;flex-direction:column;gap:8px;padding:6px 0px 0px"><p style="{XB}font-size:44px;line-height:1.2;letter-spacing:-1px;color:{NAVY}">{name}</p>{ls}</div></div>')
add('contents', f'''<section id="contents" style="background:#ffffff;color:#000000;{REG}padding:72px 0px 0px 96px;display:flex;flex-direction:column;gap:26px">
<img src="{blob('night')}" alt="밤의 정동관, 1층 상가와 6층 홀이 켜진 모습" style="position:absolute;left:1320px;top:0px;width:600px;height:1080px;object-fit:cover">
<p style="position:absolute;left:1320px;top:900px;width:560px;{SERIF}font-size:150px;line-height:1;text-align:right;white-space:nowrap;color:#ffffff;opacity:0.75">停動館</p>
<div style="display:flex;flex-direction:column;gap:8px;width:1180px">
<p style="{XB}font-size:84px;line-height:1.1;letter-spacing:-2px;color:{NAVY}">CONTENTS</p>
<p style="{BOLD}font-size:33px;line-height:1.3;color:#000000">전포 정동관 · 낮에는 주차장, 밤에는 공연과 옥상 광장</p>
<div style="display:flex;flex-direction:row;align-items:center"><div style="width:120px;height:9px;flex:none;background:{NAVY}"></div><div style="flex:1;height:2px;background:{LINE}"></div></div></div>
{cn('01','INTRODUCTION',['사업 배경 · 사업 개요'])}
{cn('02','MAIN SUBJECT',['대지 분석 · 부지 선정 근거 · 교통 및 동선 · 향·소음·조망','콘셉트 · 사례 분석 · 볼륨 도출 · 최종안 · 투시도'])}
{cn('03','CONCLUSION',['용도 선정 근거 · 층별 계획 · 단면도 · 실별 면적','동선 및 진입 계획 · 법규 검토 · 구조·방재 제안 · 확인할 것'])}
</section>
''')

# ---------------------------------------------------------------- 03 problem
rows = [['부산 전체 확보율', '130.5% (2021년 말)', '부산시 발표(파이낸셜뉴스 2022.07)'],
        ['주차환경개선지구 67곳', '평균 69.1% (2025 목표 75.6%)', '같은 자료'],
        ['부산진구 확보율(등록 대비)', '118.5% · 기준 130% 대비 약 1.7만 면 부족', '부산진구 수급실태조사(2023)'],
        ['대지 반경 500m 공영주차장', '27면 (1km 이내 약 415면)', '전국주차장정보표준데이터, 시설공단'],
        ['부산진구 불법주정차 단속', '부산 1위 (2021.1~10월 109,993건)', '글로벌경제 2021'],
        ['시 공급 계획', '2025년까지 6,092면 · 1,995억 원', '부산시 주차종합계획']]
left = col([ptitle('주차장 확보율 비교'), ptext('확보율 = 주차면수 ÷ 주차수요 × 100 · 기준선 130%', 24, GRAY, lh=1.3),
            barchart([('부산 전체(2021)', 130.5, NAVY), ('부산진구(2023)', 118.5, '#4272c4'), ('개선지구 평균', 69.1, '#8493b2')], w=760, h=250, maxv=150, ref=130),
            row([img('pk1', 372, 250, alt='전포동 이면도로의 불법주차'), img('pk2', 372, 250, alt='좁은 보도를 차지한 주차 차량')], gap=16),
            cap('전포동 이면도로 현장 사진 (답사 2026.9)', 760)], gap=12, extra='width:760px')
right = col([ptitle('수급 실태 지표'), table(['지표', '값', '출처'], [30, 41, 29], rows, 24),
             box('전포동 현황', ['▶ 이면도로 불법주차로 차량 통행 폭이 좁아지는 모습을 관찰함', '▶ 보행자가 차량을 피해 도로 중앙으로 걷는 장면을 관찰함', '▶ 답사 범위에서 상인회 사무실·주민 휴게공간을 확인하지 못함'], size=25),
             take('소규모 필지에 점포가 밀집해 부설주차장 확보가 어려워, 상권 한가운데 거점형 공영주차장이 필요함', 26)], gap=12, extra='width:900px')
add('problem', slide('problem', header('01', '사업 배경', '지역별 주차 공급 불균형', 0) + row([left, right], gap=40) + footer('파이낸셜뉴스 2022.07.11, 부산일보 2024.07.04, 글로벌경제 2021, 표준데이터 · 69.1%는 주차환경개선지구 평균', pg())))

# ---------------------------------------------------------------- 04 overview
rows = [['사업명', '전포동 복합주차장 사업 (정동관)'], ['위치', '부산진구 전포동 207번지 일대 53필지'], ['용도지역', '일반상업지역 · 방화지구'],
        ['대지면적', '4,964.5㎡ (서측 1,531.9 + 소로 733.1 + 동측 2,699.5)'], ['규모', '지하 4층 · 지상 6층 + 옥상, 지상 약 29.1m'],
        ['연면적', '43,623.7㎡ (지상 23,923.7 + 지하 19,700.0)'], ['건폐율·용적률', '87.1% (상한 90%) · 481.9% (지하 제외)'],
        ['주차', '약 600대 · 주차 비율 75.62%'], ['주요 시설', '1F 서점·카페·근생 소점포 · 5F 상인회 · 6F 가변홀 · B1~B2 공연장 200석 · 옥상 광장']]
left = col([ptitle('상세정보'), table(['구분', '내용'], [22, 78], rows, 26)], gap=12, extra='width:960px')
right = col([img('hero', 760, 428, alt='정동관 주간 투시도'), cap('주간 투시도 · 전포대로에서 본 모습', 760),
             box('停과 動', ['▶ 낮에는 상권의 차를 받는 주차장, 밤에는 지하 공연장·6F 홀·옥상 광장에 사람이 모임', '▶ 停은 차분한 전돌 스크린, 動은 붉은 순환 계단과 빛나는 홀로 드러냄'], size=25),
             ], gap=12, extra='width:780px')
add('overview', slide('overview', header('02', '사업 개요', '정동관 상세정보', 0) + row([left, right], gap=36) + take('53필지를 한 대지로 묶어 한 층 약 4,230㎡의 정형 바닥을 만들고, 두 끝을 비워 사람의 코어로 씀', 27) + footer('토지이음(2026.10.11), 본 시안 면적 계산 · 면적·대수는 개략', pg())))

# ---------------------------------------------------------------- 05 divider
ITEMS = [('INTRODUCTION', ['사업 배경 · 사업 개요']), ('MAIN SUBJECT', ['대지 분석 · 부지 선정 · 교통 및 동선 · 향·소음·조망', '콘셉트 · 사례 분석 · 볼륨 도출 · 최종안 · 투시도']), ('CONCLUSION', ['용도 선정 · 층별 계획 · 단면도 · 실별 면적', '동선 및 진입 · 법규 검토 · 구조·방재 제안'])]
add('progress-main', divider('progress-main', 1, ITEMS, 'aerial', 'MAIN SUBJECT: 대지, 부지 선정, 환경, 콘셉트, 사례, 볼륨, 최종안, 투시도'))

# ---------------------------------------------------------------- 06 site
rows = [['서측 쐐기', '19', '1,531.9', '전포대로(서)에 면한 쐐기형, 남단이 뾰족함'], ['소로 부지', '5', '733.1', '두 구역 사이 폭 약 6m, 남단 전포대로·북단 서전로'], ['동측 블록', '29', '2,699.5', '서전로·224번길·동측 이면도로에 면한 삼각형, 북단이 뾰족함'], ['합계', '53', '4,964.5', '지목 대 48필지, 도로 5필지']]
mid = col([ptitle('대지 개요'), table(['구역', '필지', '면적㎡', '형상·접도'], [17, 10, 15, 58], rows, 26, aligns=['left', 'right', 'right', 'left'], bold_rows=(3,), pad='9px 12px'),
           ptitle('배치 조건'),
           box(None, ['▶ <b>일반상업지역 · 방화지구</b>, 가로구역별 최고높이 기준 130m·최고 180m', '▶ <b>건축선 3m 이격</b>: 공연장 1,000㎡ 이상이라 북(서전로)·남(224번길)을 띄움, 전포대로 쪽은 면제', '▶ <b>두 뾰족한 끝을 비움</b>: 동측 북단 약 352㎡, 서측 남단 약 158㎡ → 개방 순환 계단 코어', '▶ 그 결과 2층 이상 건축면적 4,322.1㎡, 건폐율 <b>87.1%</b>'], size=27),
           box('확인할 것', ['207-15·79는 제3종일반주거지역도 표기됨(상업지역으로 보고 계산) · 207-84·85는 지목 대이나 도로로 쓰임'], color=GRAY, size=26)], gap=14, extra='width:1070px')
add('site', slide('site', header('01', '대지 분석', '대지 개요와 배치 조건', 1) + row([col([img('site', 640, 776, 'contain', '토지이용계획 확인도면에 서측·소로·동측 필지군을 표시한 그림', bg='#f0f3f7'), cap('토지이용계획 확인도면 · 필지군 표시(개략)', 640)], gap=8), mid], gap=36) + footer('토지이음 필지별 토지이용계획 조회(2026.10.11), 부산 건축조례 별표4 · 필지 위치는 확인도면 정합으로 판별, 치수 개략', pg())))

# ---------------------------------------------------------------- 07 selection
cards = [('1', '지하철 두 역 도보권', '1호선 서면역 737m · 2호선 전포역 529m. 주차 이용객뿐 아니라 공연·광장 방문객도 걸어서 접근함'),
         ('2', '카페거리 상권 사이', '전리단길 · 전포카페거리 · 전포사잇길 사이. 낮 방문객과 밤 관객 수요를 함께 받음'),
         ('3', '공영주차장 공백지대', '반경 500m 공영 27면, 1km 약 415면. 2022 시의회에서 대지 옆 놀이마루 부지 공영주차장 건립이 제안됨')]
cs = [f'<div style="display:flex;flex-direction:row;gap:18px;align-items:flex-start;background:{PANEL};padding:16px 22px"><p style="{XB}font-size:54px;line-height:1;width:44px;flex:none;color:{NAVY}">{n}</p><div style="display:flex;flex-direction:column;gap:6px"><p style="{BOLD}font-size:30px;line-height:1.3">{t}</p><p style="font-size:25px;line-height:1.45">{d}</p></div></div>' for n, t, d in cards]
add('selection', slide('selection', header('02', '부지 선정 근거', '수요와 접근이 맞는 곳', 1) +
    row([col([img('transit', 740, 675, 'contain', '전포동 일대 지하철역·버스정류장·상권 위치도', bg='#f0f3f7'), cap('주변 현황도 · 지도 © OpenStreetMap contributors, 위치 개략', 740)], gap=8),
         col([ptitle('입지 근거 세 가지')] + cs + [take('두 역 도보권과 카페거리 상권 사이, 공영주차장이 비어 있는 곳이라 거점형 주차장 입지로 적합함', 26)], gap=14, extra='width:1000px')], gap=36)
    + footer('카카오맵 도보 환산, 팀 상권 조사, 부산버스정보시스템(2026.9.30), 시설공단·표준데이터(2026.04), 시의회 5분 발언(2022.08)', pg())))

# ---------------------------------------------------------------- 08 access
def acc_panel(tag, color, tc, head, lines):
    ls = ''.join(f'<p style="font-size:25px;line-height:1.45">- {l}</p>' for l in lines)
    return f'<div style="display:flex;flex-direction:column;gap:6px;background:{PANEL};padding:14px 24px 16px"><div style="display:flex;flex-direction:row"><p style="{BOLD}font-size:27px;line-height:1.3;background:{color};color:{tc};padding:3px 22px">{tag}</p></div><p style="{BOLD}font-size:27px;line-height:1.4">▶ {head}</p>{ls}</div>'
add('access', slide('access', header('03', '교통 및 동선', '차량과 보행자 접근', 1) +
    row([col([img('plan1f', 700, 623, 'contain', '1층 동선도: 소로 남단 진입, 북단 진출, 가운데 횡단보도, 1층 외곽 보행', bg='#ffffff'), cap('1층 동선 개념도 · 위치와 폭은 개략', 700)], gap=8),
         col([acc_panel('차량 동선', '#00b0ef', '#000000', '남단 진입 · 북단 진출 · 소로는 차량 전용', ['전포대로에서 소로 남단으로 들어와 남→북 일방으로 이동, 북단에서 서전로로 나감', '진입·진출이 서로 만나지 않으며 400대 초과 노외주차장의 입구·출구 분리 기준을 따름']),
              acc_panel('보행 동선', '#ed7d31', '#000000', '1층 외곽을 한 바퀴', ['전포대로변, 북·남 3m 이격 마당, 동측 도로변이 보행로. 소로 중간에 횡단보도 1곳', '서점·카페·공연 로비는 전포대로 쪽에 열림']),
              acc_panel('수직 동선', '#ec8080', '#000000', '끝 코어 2곳이 사람 이동의 중심', ['개방 순환 계단 + 승강기, 지하는 같은 자리에 특별피난계단', '주차 이용객은 가까운 끝 코어로 내려와 1층 가로나 B1 로비로 감']),
              acc_panel('하역 · 이륜차', '#7030a0', '#ffffff', '동측 이면도로 쪽', ['하역 150㎡와 이륜차·자전거 주차 200㎡는 1층 동측 북쪽, 일반 차량 동선과 분리']),
              take('동측 주거 쪽에는 차량 진출입을 두지 않음', 26)], gap=10, extra='width:946px')], gap=30)
    + footer('본 시안, 주차장법 시행규칙 제5·6조 · 진출입 위치는 구청·경찰 협의 전 개념, 처리 용량은 후속 검토', pg())))

# ---------------------------------------------------------------- 09 environment
add('environment', slide('environment', header('04', '향 · 소음 · 조망', '환경 분석과 대응', 1) +
    row([col([img('env', 800, 716, 'contain', '태양 고도, 소음원, 조망축을 표시한 환경 분석도', bg='#f0f3f7'), cap('환경 분석도 · 15층 이상 건물 표시, 조망축은 개략', 800)], gap=8),
         col([box('향', ['▶ 블록 장축이 정남북, 남측 도로에 약 40m 면함', '- 태양 남중고도 동지 31.4°, 하지 78.3°(북위 35.157°)', '- 남향은 동측 1층 남단과 옥상 광장에 둠, 서측 면은 타공 스크린으로 서향 일사를 줄임'], size=27),
              box('소음', ['▶ 소음원은 서측 전포대로(광로)와 북측 서전로', '- 동측 약 45m부터 제3종일반주거지역, 실측값은 없어 낮·밤 측정이 필요함', '- 공연장은 지하, 6F 홀은 이중 차음 지붕으로 계획함'], size=27),
              box('조망', ['▶ 황령산(동 1.5km) · BIFC(남 1.2km) · 서면 도심(서 0.6km)', '- 6F(약 21m)와 옥상에서 조망, 동남동 29~30층 아파트로 6F에서는 능선 윗부분만 보일 것으로 추정함'], size=27),
              take('소음이 큰 실은 지하와 최상층 안쪽에, 남향 공간은 옥상과 1층 남단에 둠', 28)], gap=12, extra='width:940px')], gap=34)
    + footer('NOAA 태양 위치 근사식, © OpenStreetMap contributors(건물 층수), 토지이음 · 조망 앙각은 개략 추정, 소음은 실측 전', pg())))

# ---------------------------------------------------------------- 10 concept (dark)
add('concept', f'''<section id="concept" style="background:#101216;color:#ffffff;{REG}padding:0px">
<img src="{blob('night')}" alt="밤의 정동관 투시도" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover;opacity:0.55">
<div style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;background:linear-gradient(90deg, rgba(10,12,16,0.92), rgba(10,12,16,0.5) 60%, rgba(10,12,16,0.2))"></div>
<p style="position:absolute;left:150px;top:90px;width:240px;{SERIF}font-size:200px;line-height:1.05;text-align:center;color:#ffffff">停</p>
<p style="position:absolute;left:150px;top:340px;width:240px;{SERIF}font-size:200px;line-height:1.05;text-align:center;color:#ffffff">動</p>
<p style="position:absolute;left:150px;top:590px;width:240px;{SERIF}font-size:200px;line-height:1.05;text-align:center;color:#ffffff">館</p>
<p style="position:absolute;left:150px;top:900px;width:400px;{XB}font-size:64px;line-height:1.2;color:#ffffff">정동관</p>
<p style="position:absolute;left:640px;top:140px;width:1100px;{XB}font-size:84px;line-height:1.25;letter-spacing:-2px;color:#ffffff">낮에는 주차장,<br>밤에는 공연과 옥상 광장</p>
<hr style="position:absolute;left:640px;top:410px;width:420px;border-top:4px solid #ffc000">
<p style="position:absolute;left:640px;top:450px;width:1100px;{BOLD}font-size:40px;line-height:1.3;color:#ffc000">停動館의 뜻</p>
<p style="position:absolute;left:640px;top:520px;width:1100px;font-size:34px;line-height:1.7;color:#ffffff">停은 멈춤, 動은 움직임, 館은 건물임. 차가 멈추는 주차층(停)은 차분한 전돌 스크린으로 감싸고, 사람이 움직이는 계단·홀·광장(動)은 붉은 순환 계단과 빛나는 홀로 드러냄. 낮에는 상권의 차를 받고, 밤에는 지하 공연장 · 6F 가변홀 · 옥상 광장이 켜짐</p>
<p style="position:absolute;left:640px;top:880px;width:1100px;font-size:28px;line-height:1.5;color:#d9d9d9">정동관은 주차 건물이 아니라 멈춤과 움직임이 하루 안에서 교대하는 건물을 목표로 함</p>
</section>
''')

# ---------------------------------------------------------------- 11 cases 1
def case(photo, name, sub, bullets, apply, w=568):
    bl = ''.join(f'<p style="font-size:27px;line-height:1.45">- {b}</p>' for b in bullets)
    return (f'<div style="display:flex;flex-direction:column;gap:12px;width:{w}px">{img(photo, w, 380, alt=name)}'
            f'<p style="{BOLD}font-size:32px;line-height:1.25">{name}</p><p style="font-size:24px;line-height:1.3;color:{GRAY}">{sub}</p>{bl}'
            f'<div style="background:{PANEL};padding:10px 16px"><p style="font-size:27px;line-height:1.4;color:{RED};font-weight:700">적용 {apply}</p></div></div>')
add('cases-1', slide('cases-1', header('05', '사례 분석 Ⅰ', '입지 · 주차 · 공연장', 1) +
    row([case('herma', '헤르마 주차빌딩', '용인 죽전 카페거리 초입 · 2010', ['1층 상가가 계속 입점, 임대료 최고 수준 유지', '반투명 패널로 밤에 차량 불빛이 비침', '폭 14m 대지에서 램프 6m→3.3m, 삼각 보이드를 계단이 감아 오름'], '1층을 가로에 열고, 뾰족한 끝을 순환 계단 코어로'),
         case('pyeong', '평택 JS타워', '평택 · 대지 2,505㎡', ['스킵플로어로 램프 면적을 줄이고 주차 효율을 높임', '1층 근생은 층고를 반 층 높여 개방감을 줌', '알루미늄 타공판 밴드로 상층 주차부를 감쌈'], '2층 이상 스킵플로어, 줄인 램프 면적을 공연장에 배분'),
         case('blai', 'Concert House Blaibach', '독일 · Peter Haimerl · 2014', ['객석 대부분을 지하에 묻고 화강암 블록만 돌출', '지하 로비가 공연장의 완충층이 됨', '주름진 콘크리트 셸로 음향과 차음을 함께 해결'], '공연장을 B1~B2에 두고 선큰 마당으로 내려감')], gap=36)
    + footer('서울경제 2016.02.26, ArchDaily, Architect Magazine, Yatzer, 팀 조사(2026.9) · 규모·객석 수는 출처마다 달라 근거로 쓰지 않음', pg())))

# ---------------------------------------------------------------- 12 cases 2
def case2(photo, name, sub, bullets, apply, credit, w=418):
    bl = ''.join(f'<p style="font-size:26px;line-height:1.4">- {b}</p>' for b in bullets)
    ph = img(photo, w, 300, alt=name) if photo else f'<div style="width:{w}px;height:300px;background:#dae3f3;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px"><p style="{XB}font-size:44px;line-height:1.1;color:{NAVY}">985대</p><p style="font-size:26px;line-height:1.3;color:{NAVY}">지하 3층 · 지상 2층</p><p style="font-size:24px;line-height:1.3;color:{GRAY}">사진은 ArchDaily 참조</p></div>'
    return (f'<div style="display:flex;flex-direction:column;gap:8px;width:{w}px">{ph}<p style="font-size:24px;line-height:1.2;color:{GRAY}">{credit}</p>'
            f'<p style="{BOLD}font-size:30px;line-height:1.25">{name}</p><p style="font-size:24px;line-height:1.3;color:{GRAY}">{sub}</p>{bl}'
            f'<div style="background:{PANEL};padding:8px 14px"><p style="font-size:26px;line-height:1.4;color:{RED};font-weight:700">적용 {apply}</p></div></div>')
add('cases-2', slide('cases-2', header('06', '사례 분석 Ⅱ', '주차장을 머무는 곳으로', 1) +
    row([case2(None, 'Saint-Luc 주차건물', '브뤼셀 · de Jong Gortemaker Algra + MODULO · 2016', ['건물 둘레의 열린 틈(협곡)으로 지하까지 빛과 공기를 들임', '물결 모양 목재 루버 입면'], '두 끝을 비워 열린 코어로', '자유 라이선스 사진 없음'),
         case2('lincoln', '1111 Lincoln Road', '마이애미 비치 · Herzog &amp; de Meuron', ['층고 높은 주차층을 행사·문화에 탄력적으로 씀', '외기에 열려 자연환기'], '6F 가변홀 · 5F 전환 층', '© Phillip Pessar, CC BY 2.0'),
         case2('pnp', "Park 'n' Play", '코펜하겐 · JAJA Architects', ['옥상 놀이·운동 공간을 시민에게 개방', '거리에서 오르는 외부 계단'], '옥상 광장(외부 계단은 보조)', '© Leif Jørgensen, CC BY-SA 4.0'),
         case2('ballet', 'Ballet Valet', '마이애미 비치 · Arquitectonica', ['저층 상업 위에 주차 결합', '외벽 식재대와 덩굴식물로 입면 녹화'], '1층 상업 + 동측 면 녹화 검토', '© Phillip Pessar, CC BY 2.0')], gap=22)
    + footer('팀 사례 조사(2026.9), ArchDaily, Wikimedia Commons·Flickr(사진 출처 표기) · 요소별 부분 차용이며 같은 조합의 선례는 찾지 못함', pg())))

# ---------------------------------------------------------------- 13 volume
steps = [['① 53필지 합필', '서측 + 소로 + 동측 4,964.5㎡', '서측 쐐기만으로는 건축 가능 바닥이 약 920㎡라 램프가 면적을 잠식함'],
         ['② 소로 = 차량 전용 차로', '1층 층고 7m, 차로 위는 비움', '차량을 소로에 모으고 가로에는 차가 드나들지 않게 함'],
         ['③ 2층부터 한 판', '소로 위로 이은 바닥, 북·남 3m 이격', '한 층 약 4,232㎡의 정형 바닥, 법정 이격 확보'],
         ['④ 두 끝을 비워 코어로', '개방 순환 계단 + 승강기, 건폐율 87.1%', '주차가 어려운 좁은 끝을 사람 이동의 중심으로'],
         ['⑤ 스킵플로어·홀·광장', '서·동 판을 반 층 엇갈림, 6F 가변홀, 옥상 광장', '램프를 줄이고 비는 시간과 위아래 층에 공연·체육·광장을 담음']]
add('volume', slide('volume', header('07', '볼륨 도출', '필지 합필에서 최종 볼륨까지', 1) + img('steps', 1776, 352, 'contain', '볼륨 도출 5단계: 합필, 차량 전용 소로, 한 판, 두 끝 코어, 스킵플로어와 홀', bg='#ffffff') +
    table(['단계', '결정', '이유'], [22, 33, 45], steps, 27, pad='11px 14px') + take('필지를 꽉 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 곧 건물의 얼굴(순환 계단)이 됨', 28) +
    footer('본 시안(개념 볼륨 스터디) · 면적은 개략, 형태는 실제 설계안이 아님', pg())))

# ---------------------------------------------------------------- 14 final
rows = [['1층', '서측 서점·카페·공연 로비 / 소로 차량 전용 차로 / 동측 근생 소점포·램프·정산·이륜차'], ['2~4층', '스킵플로어 주차 (서측 판 7.0·10.3·13.6m, 동측 판 +1.65m)'], ['5층', '상인회·회의·공유오피스 1,200㎡ + 전환 가능 주차층'],
        ['6층·옥상', '생활체육·공연 가변홀(층고 8m) + 옥상 광장 약 1,380㎡(5F 지붕), 홀 지붕 태양광'], ['지하', 'B1·B2 공연장 200석(선큰 마당으로 진입), B3·B4 주차·설비'], ['코어', '끝 코어 2곳(지상 개방 순환 계단 + 승강기, 지하 특별피난계단) + 보조 피난계단 2곳'],
        ['외피', '주차층 전돌 스크린, 6F 세로 핀 유리(미정), 붉은 순환 계단']]
add('decision', slide('decision', header('08', '최종안', 'Final Draft와 요구·의도', 1) +
    row([col([img('aerial', 900, 506, alt='정동관 조감 투시도'), cap('조감 투시도 · 남서쪽 상공', 900),
              box('사업 요구 · 설계 의도', ['<b>요구</b> 상권의 주차 부족 해소, 이면도로 불법주차 흡수, 상인회·주민 공용 공간', '<b>의도</b> 주차를 한 블록에 모으고, 비는 시간과 위아래 층에 공연·체육·광장을 담음'], size=27)], gap=10),
         col([ptitle('최종안 요약'), table(['구분', '내용'], [15, 85], rows, 27, pad='10px 12px'),
              box('수치', ['대지 4,964.5㎡ · 건축면적 4,322.1㎡ (건폐율 87.1%) · 연면적 43,623.7㎡ · 용적률 481.9% · 높이 29.1m · 주차 약 600대'], color=NAVY, size=26)], gap=12, extra='width:830px')], gap=36)
    + footer('본 시안(면적 계산·투시도), 주차장법 제12조의2 · 모든 수치는 개략', pg())))

# ---------------------------------------------------------------- 15-17 renders
def render_slide(sid, n, title, sub, big, bigcap, small, smallcap, notes, src, tk=''):
    return slide(sid, header(n, title, sub, 1) +
        row([col([img(big[0], 1260, 709, alt=big[1]), cap(bigcap, 1260)], gap=6),
             col([img(small[0], 490, 276, alt=small[1]), cap(smallcap, 490)] + notes, gap=10, extra='width:490px')], gap=26) + take(tk, 28) + footer(src, pg()))
add('render-1', render_slide('render-1', '09', '투시도 Ⅰ', '주간 외관', ('hero', '전포대로에서 본 주간 투시도'), '전포대로(서측)에서 본 주간 외관 · 전돌 스크린과 붉은 순환 계단', ('street', '서전로와 전포대로 모퉁이에서 본 주간 투시도'), '서전로 × 전포대로 모퉁이 · 1층 서점·카페가 전포대로를 향해 열림',
    [box(None, ['▶ 주차층(停)은 타공 전돌 스크린으로 감싸 서향 일사와 소음을 줄임', '▶ 동(動)의 코어는 붉은 순환 계단으로 드러나 건물의 얼굴이 됨', '▶ 6F 홀은 세로 핀 유리(외피 미정)'], size=25, lh=1.4)], '투시도: 개념 볼륨 모델 + OpenStreetMap 높이 자료(주변 건물 단순화) · 실제 설계안이 아님', '停은 전돌 스크린으로 조용하게, 動은 붉은 순환 계단으로 눈에 띄게 — 한 건물 안에서 두 얼굴을 나눔'))
add('render-2', render_slide('render-2', '10', '투시도 Ⅱ', '밤과 소로', ('night', '밤의 정동관 투시도'), '밤의 전포대로변 · 주차층은 어둡게, 1층·6F 홀·순환 계단이 켜짐', ('lane', '소로 안에서 본 차량 전용 차로'), '소로 안 · 남→북 일방 차로, 위는 2층 바닥으로 덮임',
    [box(None, ['▶ 밤에는 지하 공연장·6F 홀·1층 상가가 켜지고 주차층은 낮은 조도로 남음', '▶ 소로는 7m 높이로 덮인 차량 전용 통로, 보행은 1층 외곽으로 분리'], size=25, lh=1.4)], '투시도: 개념 볼륨 모델 · 조명 계획은 개념, 소음·조명 운영시간은 후속', '밤에는 켜지는 곳이 곧 사람이 모이는 곳 — 주차장이 공연장과 광장으로 바뀌어 보임'))
add('render-3', render_slide('render-3', '11', '투시도 Ⅲ', '옥상 광장과 선큰 마당', ('roof', '옥상 광장에서 본 투시도'), '5F 지붕 옥상 광장(+21.1m) · 잔디·벤치·플랜터, 맞은편 6F 가변홀', ('sunken', '끝 코어② 선큰 마당과 붉은 순환 계단'), '끝 코어② · 선큰 마당으로 내려가 B1 공연장 로비에 닿음(Blaibach 개념)',
    [box(None, ['▶ 옥상 광장은 홀 옆 5F 지붕 위, 약 1,380㎡', '▶ 순환 계단은 지상에서 옥상까지 이어지고 지하는 특별피난계단이 같은 자리에 놓임'], size=25, lh=1.4)], '투시도: 개념 볼륨 모델 · 광장 시설 배치는 개념', '옥상 광장과 지하 선큰 마당이 같은 순환 계단 코어로 이어져 위아래 모두 사람이 모이는 곳이 됨'))

# ---------------------------------------------------------------- 18 divider conclusion
add('progress-concl', divider('progress-concl', 2, ITEMS, 'night', 'CONCLUSION: 용도·층별 계획, 단면, 면적, 동선, 법규, 제안'))

# ---------------------------------------------------------------- 19 program
rows = [['주차장', 'B4~5F, 1F 램프', '32,988.4', '부산진구 확보율 118.5%(기준 130%), 반경 500m 공영 27면'], ['공연장 200석', 'B1~B2', '1,900', '1km 안에 객석형 소극장 없음, 지하는 전포대로 소음에 강함'],
        ['생활체육·공연 가변홀', '6F', '2,850 (+코어 150)', '1km 안에 공연 겸용 가변 홀이 없음, 행사에 따라 객석·코트를 바꾸는 가변형'], ['서점·카페·근생 소점포', '1F', '1,400', '카페거리 방문객을 건물로 유도, 근생은 10곳 안팎 소점포로 나눠 가로의 결을 이음'],
        ['상인회·공유오피스', '5F', '1,200', '답사 범위에서 상인회 사무실을 확인하지 못함'], ['옥상 광장', '5F 지붕', '약 1,380 (옥외)', '쉼터·공용 공간 부족, 밤에는 공연과 이어 개방']]
rows2 = [['객석형 소극장', '없음 (지하 라이브클럽 1곳)', '없음 (스탠딩 라이브홀·연회장·1,727석 대극장)'], ['공공 체육관', '없음', '국민체육센터 0.73km(다목적체육관 1,394㎡, 황령산 경사지)'], ['공연 겸용 가변 홀', '없음', '없음']]
add('program', slide('program', header('01', '용도 선정 근거', '용도 여섯 가지와 반경 내 현황', 2) +
    ptitle('용도별 위치와 선정 근거') + table(['용도', '위치', '면적㎡', '선정 근거'], [20, 12, 16, 52], rows, 26, aligns=['left', 'left', 'right', 'left'], pad='8px 12px') +
    ptitle('반경 내 현황조사 (대지 중심 직선거리)') + table(['구분', '500m 안', '1km 안'], [22, 30, 48], rows2, 26, pad='8px 12px') +
    take('주차가 중심이고, 나머지 용도는 비는 시간과 위아래 층을 채움 · 공연·체육 시설은 반경 내 공백 유형(소극장, 공연 겸용 홀)에 맞춤', 26) +
    footer('부산진구 문화시설·공공체육시설현황(data.go.kr), 부산시 공연장목록, 현장 답사(2026.9), 본 시안 · 미등록 민간 공간은 빠졌을 수 있음', pg())))

# ---------------------------------------------------------------- 20 floors
def fl(h, bg, left, right, lh=None):
    return f'<div style="display:flex;flex-direction:row;align-items:center;justify-content:space-between;height:{h}px;background:{bg};border:2px solid #000000;padding:0px 22px"><p style="font-size:26px">{left}</p><p style="{BOLD}font-size:26px">{right}</p></div>'
stack = col([ptitle('층별 쓰임과 층고'),
             fl(58, '#e2f0d9', '옥상 광장 · 녹지 · 벤치 (밤 개방, 5F 지붕) 약 1,380㎡', 'RF'),
             fl(88, '#8faadc', '생활체육·공연 가변홀 · 층고 8.0m · 3,000.0㎡', '6F'),
             fl(62, '#d9cbe9', '상인회·회의·공유오피스 + 전환 가능 주차 · 4.2m · 4,322.1㎡', '5F'),
             fl(128, '#c9c9c9', '스킵플로어 주차 · 3.3m · 층당 4,322.1㎡ (동측 판 +1.65m)', '2~4F'),
             fl(98, '#fbf3a4', '서점·카페·공연 로비 / 차로 / 근생·램프·이륜차 · 7.0m(동 8.65m) · 3,635.3㎡', '1F'),
             f'<div style="display:flex;flex-direction:row;align-items:center;gap:14px"><div style="flex:1;height:0px;border-top:3px dashed #000000"></div><p style="font-size:24px;color:{GRAY}">지반선</p><div style="flex:1;height:0px;border-top:3px dashed #000000"></div></div>',
             fl(110, '#9dc3e6', '공연장 200석 + 주차 · 4.5m · 4,806.5 / 4,964.5㎡', 'B1~B2'),
             fl(110, '#c9c9c9', '주차 + 전기·펌프·저수조 · 3.3m · 층당 4,964.5㎡', 'B3~B4')], gap=6, extra='width:1000px')
side = col([img('secB', 360, 411, 'contain', 'B 횡단면: 서측 판, 소로, 동측 판이 반 층 엇갈린 스킵플로어', bg='#ffffff'), cap('횡단면 B · 서·동 판이 반 층 엇갈림', 360),
            box('높이 · 연면적', ['▶ 지상 약 29.1m, 지하 약 15.6m', '- 지상 23,923.7 + 지하 19,700.0 = 43,623.7㎡'], size=24, w=360)], gap=8, extra='width:360px')
hall = box('6F 가변홀 (가변형)', ['홀 1,500㎡: 생활체육(배드민턴·풋살 수준) ↔ 공연·행사(가변 객석). 유효 높이 약 6m라 농구·배구 공식 경기는 대상에서 뺌', '수용 인원은 행사 형태에 따라 바뀌는 가변형'], color=NAVY, size=24, w=380)
add('floors', slide('floors', header('02', '층별 계획', '층별 쓰임과 층고', 2) + row([stack, side, hall], gap=26) +
    footer('공연장 조성 매뉴얼(예술경영지원센터, 2008) 조닝 원칙, 본 시안 · 층고·면적 개략', pg())))

# ---------------------------------------------------------------- 21 sections
add('sections', slide('sections', header('03', '단면도 Ⅰ', '소로를 따라 펼친 종단면', 2) +
    row([col([img('secA', 1400, 639, 'contain', 'A 종단면: 소로를 따라 펼친 단면, 두 끝 코어와 지하 공연장', bg='#ffffff'), cap('A 종단면 · 소로를 따라 펼친 개념 단면 (남 → 북)', 1400)], gap=6),
         col([img('keyplan', 340, 590, 'contain', '단면선 위치를 표시한 1층 키 플랜', bg='#ffffff'), cap('단면선 위치', 340)], gap=6)], gap=34) +
    row([box(None, ['▶ <b>남쪽 근생 → 끝 코어②</b> 구간: 개방 순환 계단, 지하는 선큰 마당·공연장', '▶ <b>램프·정산</b> 구간을 지나 <b>끝 코어①</b> 구간: 순환 계단 + 승강기'], size=27, w=1000, lh=1.4),
         box(None, ['▶ 두 끝은 지상에서 비어 있고 지하는 특별피난계단', '▶ 지하 공연장은 선큰 마당으로 빛이 닿음'], color=GRAY, size=27, w=742, lh=1.4)], gap=34) +
    footer('본 시안 개념 단면 · 구조·설비 두께는 표현하지 않음, 층고·면적 개략', pg())))
add('sections-b', slide('sections-b', header('04', '단면도 Ⅱ', '횡단면: 스킵플로어', 2) +
    row([col([img('secB', 612, 700, 'contain', 'B 횡단면: 서측 판, 소로, 동측 판이 반 층 엇갈린 스킵플로어', bg='#ffffff'), cap('B 횡단면 (y=70m 지점)', 612)], gap=6),
         col([box('B 횡단면', ['y=70m 지점. 서측 판(7.0·10.3·13.6m)과 동측 판(+1.65m)이 소로 위에서 반 층 엇갈려 스킵플로어를 이룸'], size=29, lh=1.45),
              box('스킵플로어 효과', ['▶ 램프 길이를 줄여 층 이동을 짧게 함', '▶ 소로가 두 판 사이의 이음매가 되고, 소로 위는 2층 바닥으로 덮여 차로 높이는 7m', '▶ 서측 판 4개 레벨과 동측 판 3개 레벨이 반 층씩 어긋나 각 층 한쪽은 가로와 가깝게 열림'], size=29, lh=1.45),
              box('지하 공연장', ['▶ 지하 공연장(B1~B2)은 박스인박스와 방진 바닥으로 차량 진동을 차단하는 방향을 제안', '▶ 객석은 선큰 마당 쪽 로비에서 내려가 진입'], color=GRAY, size=29, lh=1.45),
              take('서·동 판이 반 층 엇갈려 램프를 짧게 하고, 소로가 이음매가 됨', 28)], gap=14, extra='width:1100px')], gap=34) +
    footer('본 시안 개념 단면 · 구조·설비 두께는 표현하지 않음, 층고·면적 개략', pg())))

# ---------------------------------------------------------------- 22 area above
fl_rows = lambda keys: [[k if i == 0 else '', n, f'{v:,.1f}', f'{v / 3.3058:,.0f}'] for k in keys for i, (n, v, c) in enumerate(AR['floors'][k]['rows'])]
def area_tab(keys, size=26, pad='7px 10px'):
    rs = []; bi = []; bold = []
    for bi_idx, k in enumerate(keys):
        rows_ = AR['floors'][k]['rows']
        for i, (n, v, c) in enumerate(rows_):
            rs.append([k if i == 0 else '', n, f'{v:,.1f}', f'{v / 3.3058:,.0f}']); bi.append(bi_idx)
        t = AR['tot'][k]; rs.append(['', f'<b>{k} 합계</b>', f'<b>{t:,.1f}</b>', f'{t / 3.3058:,.0f}']); bi.append(bi_idx)
    return table(['층', '실', '면적㎡', '평'], [13, 51, 21, 15], rs, size, aligns=['left', 'left', 'right', 'right'], band_by=bi, lh=1.2, pad=pad)
add('area-above', slide('area-above', header('05', '실별 면적', '지상층', 2) +
    row([col([ptitle('6F · 5F · 2~4F(층당)'), area_tab(['6F', '5F']), area_tab(['4F']).replace('4F', '2~4F', 1)], gap=10, extra='width:860px'),
         col([ptitle('1F와 연면적'), area_tab(['1F']),
              box(None, [f'<b>지상 연면적</b> 23,923.7㎡ (7,237평) · <b>지하</b> 19,700.0㎡ (5,959평)', '<b>전체 연면적 43,623.7㎡ (13,196평)</b>', '건축면적 4,322.1㎡ · 건폐율 87.1% · 용적률 481.9%(지하 제외)'], size=25),
              ptext('1F의 소로 차로 686.8㎡는 필로티 차로로 바닥면적에서 제외, 옥상 광장 약 1,380㎡는 옥외', 24, GRAY, lh=1.35)], gap=10, extra='width:880px')], gap=36)
    + footer('본 시안 면적 계산(1평 = 3.3058㎡) · 3m 이격·끝 코어 2곳·보조 피난계단 2곳 반영, 모든 면적은 개략', pg())))

# ---------------------------------------------------------------- 23 area below
vals = [AR['cat'][k] for k in ('park', 'cult', 'biz', 'core')] + [AR['cat']['sup'] + AR['cat']['mep']]
cols = ['#08205e', '#4272c4', '#7f9dcf', '#abbde0', '#dbe2f5']
labs = [('주차장(램프·정산·이륜차 포함)', 'park'), ('문화·공연', 'cult'), ('상업·상인', 'biz'), ('코어', 'core')]
leg = [f'<p style="font-size:24px;line-height:1.3"><span style="color:{c}">■</span> {n} {AR["cat"][k] / AR["gfa"] * 100:.2f}% · {AR["cat"][k]:,.1f}㎡</p>' for (n, k), c in zip(labs, cols)]
leg.append(f'<p style="font-size:24px;line-height:1.4"><span style="color:{cols[4]}">■</span> 설비·지원 {(AR["cat"]["sup"] + AR["cat"]["mep"]) / AR["gfa"] * 100:.2f}% · {AR["cat"]["sup"] + AR["cat"]["mep"]:,.1f}㎡</p>')
add('area-below', slide('area-below', header('06', '실별 면적', '지하층과 구성비', 2) +
    row([col([ptitle('B1 · B2'), area_tab(['B1', 'B2'], 25, '6px 10px'),
              box(None, ['<b>지하 연면적 19,700.0㎡</b> (5,959평) · 층당 4,806.5~4,964.5㎡', '지하 코어는 특별피난계단 4곳 포함 층당 150㎡, B1은 선큰 마당(약 158㎡, 옥외)을 뺀 면적'], size=24, lh=1.4)], gap=10, extra='width:860px'),
         col([ptitle('B3 · B4'), area_tab(['B3', 'B4'], 25, '6px 10px'),
              row([f'<div style="position:relative;width:250px;height:250px;flex:none">{donut(vals, cols, size=250, r_out=114, r_in=66)}<p style="position:absolute;left:35px;top:92px;width:180px;{XB}font-size:36px;line-height:1.1;text-align:center;color:{NAVY}">75.62%</p><p style="position:absolute;left:35px;top:134px;width:180px;font-size:24px;line-height:1.3;text-align:center;color:{GRAY}">주차장</p></div>',
                   col(leg, gap=2)], gap=14, align='center')], gap=10, extra='width:860px')], gap=40)
    + footer('본 시안 면적 계산 · 주차 비율 75.62%(요건 70% 이상) · 주차는 약 600대로 표기 · 면적은 개략', pg())))

# ---------------------------------------------------------------- 24 circulation
def lg_item(sw, text):
    return row([sw, f'<p style="font-size:25px;line-height:1.3">{text}</p>'], gap=12, align='center')
sq = lambda c: f'<div style="width:28px;height:28px;flex:none;background:{c};border:2px solid #000000"></div>'
leg_grid = grid('1fr 1fr', [lg_item(sq('#fbf3a4'), '상업·문화(서점·카페·로비·근생)'), lg_item(sq('#f4d3b0'), '주차 관련(램프·정산·이륜차)'), lg_item(sq('#8c8c8c'), '소로 = 차량 전용(일방 남→북)'), lg_item(sq('#ec8080'), '끝 코어(순환 계단 + 승강기)'), lg_item(sq('#fff3e3'), '건축선 3m 이격 = 보행 마당'),
                lg_item('<div style="width:28px;height:0px;flex:none;border-top:5px dashed #ed7d31"></div>', '보행 동선(1층 외곽)'), lg_item('<div style="width:28px;height:7px;flex:none;background:#00b0ef"></div>', '차량 진입·진출'), lg_item('<div style="width:28px;height:28px;flex:none;background:#c00000"></div>', '보조 계단')], gap=10, extra='padding:0px')
legend = col([row([pill('범례', GRAY, size=26)]), leg_grid], gap=10, extra=f'background:{PANEL};padding:14px 24px 16px')
add('circulation', slide('circulation', header('07', '동선 및 진입 계획', '1층 배치와 수직 동선', 2) +
    row([col([img('plan1f', 486, 807, 'contain', '1층 평면 개념과 동선', bg='#ffffff')], gap=0),
         col([legend,
              box('1층 배치', ['▶ <b>서측 쐐기</b>: 북쪽부터 서점 400㎡, 카페 400㎡, 공연 로비 300㎡, 전포대로변으로 열림', '▶ <b>소로</b>: 차량 전용 차로(남→북 일방), 가운데 횡단보도 1곳', '▶ <b>동측 블록</b>: 남쪽 근생 소점포 600㎡(10곳 안팎), 가운데 램프·정산, 북쪽 이륜차·자전거 200㎡와 하역', '▶ <b>북·남 3m 이격 마당</b>이 건물을 한 바퀴 도는 보행로가 됨'], size=25, lh=1.4),
              box('수직 동선', ['▶ 끝 코어 2곳이 사람 이동의 중심: 지상 개방 순환 계단 + 승강기, 지하 특별피난계단', '▶ 주차 이용객은 가까운 끝 코어로 내려와 1층 가로나 B1 공연장 로비로 감', '▶ 공연 관객은 전포대로 → 끝 코어② 계단 → 선큰 마당 → B1 로비로 내려감'], size=25, lh=1.4),
              box('확인할 것', ['처리 용량(피크 대기행렬) · 소로 남단이 224번길 모퉁이·횡단보도·정류장과 떨어진 거리'], color=GRAY, size=25, lh=1.4)], gap=10, extra='width:1260px')], gap=30)
    + footer('본 시안 · 진출입 위치는 구청·경찰 협의 전 개념이며 도면은 개략', pg())))

# ---------------------------------------------------------------- 25-26 legal
lg1 = [['주차전용건축물 요건', '주차장법 시행령 제1조의2①', '주차 외 용도가 근생·문화집회·운동·업무 등이면 주차 70% 이상', '75.62%', '적합'],
       ['건폐율', '주차장법 제12조의2', '90% 이하', '87.1% (4,322.1㎡)', '적합'], ['용적률', '같은 조', '1,500% 이하', '481.9% (지하 제외)', '적합'],
       ['대지 안의 공지', '부산 건축조례 별표4, 건축법 시행령 별표2', '문화집회 1,000㎡ 이상: 건축선에서 3m (너비 20m 이상 도로 쪽 면제)', '북·남 3m, 전포대로 0m', '적합(반영)'],
       ['높이', '건축법 제60·61조', '가로구역 최고 180m, 일조 제한은 주거지역만', '29.1m', '적합'], ['용도 분류', '건축법 시행령 별표1', '공연장 500㎡ 이상은 문화 및 집회시설', '1,900㎡', '문화 및 집회시설']]
lg2 = [['노외주차장 출입구', '주차장법 시행규칙 제5조', '400대 초과 시 입구·출구 분리, 교차로·횡단보도 5m·정류장 10m 안 금지', '남단 진입·북단 진출 분리', '조건부(진입부 거리 확인)'],
       ['주차장 구조', '같은 규칙 제6조', '경사로 직선 17%·곡선 14% 이하, 직각주차 차로 6.0m, 주차부분 높이 2.1m', '층고 3.3m, 반 층 램프', '조건부(설계 단계)'],
       ['의무 구획', '같은 규칙, 부산 주차장조례, 친환경차법 시행령', '확장형 30%, 장애인 3%, 친환경차 5%, 충전기 5%', '약 600대 기준 180·18·30·30기(급속 10)', '반영 예정'],
       ['부설주차장', '부산 주차장조례 별표7', '주차전용건축물 안 주차 외 시설은 면제', '공연장·근생·업무', '면제'],
       ['피난', '건축법 시행령 제34·35조', '보행거리 50m(지하 공연장 30m), 지하 3층 이하 특별피난계단', '끝 코어 2 + 보조 2, 지하 특피 4', '조건부(작도 필요)'],
       ['비상용 승강기', '건축법 제64조', '높이 31m 초과 시', '29.1m', '해당 없음']]
def legal(sid, n, title, sub, rows_, note):
    return slide(sid, header(n, title, sub, 2) + table(['항목', '조문', '기준', '계획값', '판정(참고)'], [14, 20, 31, 20, 15], rows_, 28, pad='12px 14px') + note +
        footer('law.go.kr 현행본(2026.10.11 조회) · 판정은 참고용이며 최종 판단은 원문으로 다시 확인함', pg()))
add('legal-1', legal('legal-1', '08', '법규 검토 Ⅰ', '배치·규모', lg1, box('계획에 반영한 것', ['건폐율 100% → 87.1%: 두 끝을 코어로 비우고 북·남 3m 이격 · 용적률은 주차전용건축물 특례 한도(1,500%)에 크게 못 미침'], size=30) + take('규모 한도는 건폐율이 지배 조건이며, 이를 두 끝 코어와 3m 이격으로 풀었음', 28)))
add('legal-2', legal('legal-2', '09', '법규 검토 Ⅱ', '주차·피난·기타', lg2, box('후속 확인', ['진입부와 224번길 모퉁이·횡단보도·정류장 거리 · 개방 순환 계단의 피난계단 인정 여부 · 보행거리 작도(코어 4곳 기준 50m, 지하 공연장 30m)'], color=GRAY, size=30) + take('피난과 출입구는 조건부이며 설계 단계에서 작도와 거리 확인으로 해소함', 28)))

# ---------------------------------------------------------------- 27 proposal
def prop(tag, head, lines):
    ls = ''.join(f'<p style="font-size:31px;line-height:1.5">- {l}</p>' for l in lines)
    return f'<div style="display:flex;flex-direction:column;gap:12px;background:{PANEL};padding:20px 24px 24px;width:560px"><div style="display:flex;flex-direction:row"><p style="{BOLD}font-size:29px;line-height:1.3;background:{NAVY};color:#ffffff;padding:3px 22px">{tag}</p></div><p style="{BOLD}font-size:34px;line-height:1.35">{head}</p>{ls}</div>'
add('proposal', slide('proposal', header('10', '구조·방재 제안', '뒷부분 제안 · 검토 필요', 2) +
    row([prop('구조 제안', '주차 모듈에 맞춘 기둥 격자', ['기둥 격자는 주차 구획 모듈에 맞춰 약 7.5~8.1m 단위로 제안', '6F 가변홀(1,500㎡)은 트러스·전이보로 무주 공간을 확보, 스팬과 유효 높이(약 6m) 검토', '서·동 두 판의 반 층 차이는 접합부 전이로 처리', '지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단']),
         prop('방재·피난 제안', '지하 공연장과 순환 계단', ['지하 공연장은 방화구획과 전용 특별피난계단(보행거리 30m)', '끝 코어 2곳 + 보조 계단 2곳, 보행거리 50m 작도로 확인', '개방 순환 계단이 피난계단으로 인정되는지 검토', '주차층은 스프링클러·제연, 전기차 충전 구획은 방화 대책과 함께']),
         prop('설비·운영 제안', '자연환기와 후속 과제', ['개방 외피로 주차층 자연환기, 지하는 기계환기와 CO 센서', '확장형 180·장애인 18·친환경차 30·충전기 30기(급속 10)', '소음·조명 운영시간, 처리 용량(피크 대기행렬)은 후속 검토', '5F 전환 층은 차량이 줄면 다른 용도로 바꾸는 여지'])], gap=26) +
    take('구조·방재는 확정 설계가 아니라 제안이며, 설계 단계에서 작도와 계산으로 검증함', 29) + footer('본 시안 제안 · 법규 판정과 구조 계산은 설계 단계에서 확인', pg())))

# ---------------------------------------------------------------- 28 open
rows = [['1', '약 600대와 주차 면적 약 33,000㎡의 관계', '1대당 약 55㎡로 계산돼 효율이 낮다는 지적 가능 → 기준층 배치로 확인'], ['2', '진입부(소로 남단)와 224번길 모퉁이·횡단보도·정류장 거리', '출입구 설치 금지 구간(5m·10m)'],
        ['3', '개방 순환 계단의 피난계단 인정 여부', '안 되면 보조 피난계단 2곳이 법정 계단 역할'], ['4', '대지 안의 공지의 지하층 적용 여부', '지금은 지하를 대지 전체로 계산'], ['5', '207-15·79 용도지역 표기', '제3종일반주거지역 동시 표기'],
        ['6', '보행거리 작도(코어 4곳 기준 50m, 지하 공연장 30m)', '피난 조건부 판정 해소'], ['7', '6F 외피 재료, 소음·조명 운영시간, 처리 용량', '후속 설계 과제']]
add('open', slide('open', header('11', '확인할 것', '한계와 다음 단계', 2) + table(['#', '확인할 것', '이유·방향'], [6, 46, 48], rows, 29, pad='13px 16px') +
    box('이번 판에서 다루지 않은 것', ['사업성(토지 매입·공사비·주차 수입) · 합필 방식과 운영 주체 · 침수·지반 · 소음 실측 · 투시도 외 도면(평면·단면 상세)'], color=GRAY, size=28) +
    take('수치는 모두 개략이며, 확정은 법규 원문 확인과 설계 단계의 작도에서 이뤄짐', 28) + footer('본 시안 · 정동관 내용 문서의 열린 이슈와 같은 항목', pg())))

# ---------------------------------------------------------------- 29 thanks
add('thanks', f'''<section id="thanks" style="background:#141414;color:#ffffff;{REG}padding:0px">
<img src="{blob('aerial')}" alt="정동관 조감 투시도" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover;opacity:0.5">
<p style="position:absolute;left:96px;top:150px;width:1500px;{SERIF}font-size:280px;line-height:1.05;letter-spacing:6px;white-space:nowrap;color:#ffffff;opacity:0.9">停動館</p>
<p style="position:absolute;left:96px;top:560px;width:1300px;{XB}font-size:120px;line-height:1.1;color:#ffffff">THANK YOU</p>
<p style="position:absolute;left:96px;top:830px;width:1300px;{BOLD}font-size:48px;line-height:1.3;color:#ffc000">전포 정동관 · 낮에는 주차장, 밤에는 공연과 옥상 광장</p>
<p style="position:absolute;left:96px;top:930px;width:1300px;font-size:32px;line-height:1.4;color:#ffffff">202325137 정성윤</p>
</section>
''')

# ---------------------------------------------------------------- deck.json
order = [s for s, _ in SL]
deck = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-11T15:00:00Z"}, "lists": "css", "title": "전포 정동관 · 전체본 (공설기 v1.2)", "cover": "cover", "order": order,
        "sections": {"s1": {"description": "INTRODUCTION: 표지, 목차, 사업 배경과 개요", "start": "cover"}, "s2": {"description": "MAIN SUBJECT: 대지, 부지 선정, 환경, 콘셉트, 사례, 볼륨, 최종안, 투시도", "start": "progress-main"}, "s3": {"description": "CONCLUSION: 용도, 층별, 단면, 면적, 동선, 법규, 제안", "start": "progress-concl"}},
        "faces": {"pretendard": {"family": "Pretendard", "src": "project/ds/gongseolgi/fonts/Pretendard-Regular.woff2"}, "pretendard-bold": {"family": "Pretendard Bold", "src": "project/ds/gongseolgi/fonts/Pretendard-Bold.woff2"},
                  "pretendard-extrabold": {"family": "Pretendard ExtraBold", "src": "project/ds/gongseolgi/fonts/Pretendard-ExtraBold.woff2"}, "noto-serif-kr": {"family": "Noto Serif KR", "href": "https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@900&display=swap"}},
        "designSystems": [{"title": "공설기 v1.2", "namespace": "gongseolgi", "artifact": "https://claude.ai/artifact/L945L4Rv5pmxj397Xkt7cY", "version": "1791713228-b453", "copiedAt": "2026-10-11T15:00:00Z"}]}
json.dump(deck, open(D + 'full/project/deck.json', 'w'), ensure_ascii=False, indent=1)
print(len(order), order)
