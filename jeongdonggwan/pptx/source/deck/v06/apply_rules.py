# jinba slide-rules §2/§4.8/§4.20 applied on top of 공설기 v1.2:
#   - the sub-title slot of the term header carries the conclusion (a sentence, 함/임)
#   - no bottom conclusion band anywhere; so-what is in the header or in a right-hand section
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('deck.js', encoding='utf8').read()
n = 0


def sub(old, new):
    global s, n
    assert s.count(old) == 1, (s.count(old), old[:60])
    s = s.replace(old, new); n += 1


# ---- header sentences
sub("S('사업 배경 Ⅰ', '사람을 받아 온 땅, 이번에는 차와 사람을 함께 받을 차례', 0,", "S('사업 배경 Ⅰ', '사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임', 0,")
sub("S('사업 배경 Ⅱ', '먹고 · 보고는 채워졌고, 듣고가 비어 있음', 0,", "S('사업 배경 Ⅱ', '먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함', 0,")
sub("S('사업 배경 Ⅲ', '주차장과 공연장은 한 건물이어야 함', 0,", "S('사업 배경 Ⅲ', '주차장이 공연장을 받치고 공연장이 주차장을 살림', 0,")
sub("S('대지 분석', '53필지를 한 블록으로 쓰는 조건', 1,", "S('대지 분석', '53필지를 합쳐 한 블록으로 쓸 수 있는 대지임', 1,")
sub("S('부지 선정', '왜 꼭 이 땅인가', 1,", "S('부지 선정', '수요 · 공백 · 형상이 모두 이 땅에 겹침', 1,")
sub("S('향 · 일조', '남북 장축 블록의 일사와 그림자', 1,", "S('향 · 일조', '서 · 동 면은 슬랫으로 거르고 광장은 남쪽에 둠', 1,")
sub("S('소음', '서 · 북 도로변 소음원과 동측 주거 경계', 1,", "S('소음', '소음 큰 실은 지하 · 최상층 안쪽에 두고 서 · 북 면은 닫음', 1,")
sub("S('조망', '황령산 · BIFC · 서면 도심', 1,", "S('조망', '조망은 옥상 광장에서 얻고 남 · 동으로만 엶', 1,")
sub("caseSlide('사례 분석 Ⅰ', '좁은 상업 대지의 주차빌딩',", "caseSlide('사례 분석 Ⅰ', '좁은 대지의 주차빌딩은 램프를 줄이고 1층을 열었음',")
sub("caseSlide('사례 분석 Ⅱ', '주차 건물의 외피와 옥상',", "caseSlide('사례 분석 Ⅱ', '외피는 슬랫으로 감싸고 옥상은 시민에게 열었음',")
sub("caseSlide('사례 분석 Ⅲ', '공연과 행사를 담는 구조',", "caseSlide('사례 분석 Ⅲ', '공연과 행사는 지하 홀과 높은 층고에 담았음',")
sub("S('볼륨 도출', '필지 합필에서 최종 볼륨까지', 1,", "S('볼륨 도출', '두 끝을 비워 이격을 맞추고 그 자리를 얼굴로 씀', 1,")
sub("S('최종안', 'Final Draft와 요구 · 의도', 1,", "S('최종안', '주차 75.62%로 요건을 맞추고 공연과 광장을 얹음', 1,")
sub("renderSlide('투시도 Ⅰ', '주간과 밤, 목재 슬랫 외피',", "renderSlide('투시도 Ⅰ', '주차층은 슬랫으로 감싸고 홀과 계단은 켜서 드러냄',")
sub("renderSlide('투시도 Ⅱ', '옥상 광장 · 끝 코어 · 소로',", "renderSlide('투시도 Ⅱ', '옥상 광장과 소로가 보행과 차량을 한 건물에서 나눔',")
sub("S('용도 선정 · 층별 계획', '용도 여섯 가지와 층별 쓰임', 2,", "S('용도 선정 · 층별 계획', '반경 안에 없는 용도 여섯 가지를 층별로 쌓음', 2,")
sub("S('단면도', '소로를 따라 펼친 종단면과 횡단면', 2,", "S('단면도', '소로를 따라 자른 단면에서 차와 사람의 길이 갈림', 2,")
sub("S('실별 면적', '지상 · 지하 면적과 구성비', 2,", "S('실별 면적', '주차 비율 75.62%로 주차전용건축물 요건을 충족함', 2,")
sub("S('동선 및 진입 계획', '1층 배치와 수직 동선', 2,", "S('동선 및 진입 계획', '차량은 소로로, 보행은 1층 외곽으로 나눔', 2,")
sub("S('법규 검토 · 구조 · 방재 제안', '계획값과 조건부 항목', 2,", "S('법규 검토 · 구조 · 방재 제안', '적합 3건 · 조건부 3건, 구조 · 방재는 제안 수준임', 2,")
sub("S('사례 차용 외피 대안', 'Saint-Luc · 1111 Lincoln Road · Blaibach', 2,", "S('사례 차용 외피 대안', '같은 매스에 사례의 외피 방식만 바꿔 비교함', 2,")
sub("S('형태 대안 3종', '같은 대지, 다른 매스 · 규모는 비슷하게 유지', 2,", "S('형태 대안 3종', '같은 대지에서 매스만 바꾸면 바닥면적이 최대 19% 줄어듦', 2,")
sub("S('확인할 것', '한계와 다음 단계', 2,", "S('확인할 것', '남은 일은 법규 원문 확인과 작도임', 2,")

# ---- remove the remaining bottom bands (so-what now lives in the header sentence)
parts = re.split(r'(?m)^(?=// =+  )', s)
out = []
for blk in parts:
    head = blk.split('\n', 1)[0]
    if any(k in head for k in ('01 사업 배경 Ⅰ', '02 사업 배경 Ⅱ', '04 부지 선정', '04 향', '05 소음', '06 조망')):
        b = re.sub(r"const cH = conclusionHeight\([^;]*\);", "const cH = -SP.s2;", blk, count=1)
        b = re.sub(r"\n  conclusion\([^;]*\);", "", b, count=1)
        assert b != blk, head
        blk = b
        n += 1
    out.append(blk)
s = ''.join(out)
open('deck.js', 'w', encoding='utf8').write(s)
print('edits', n)
