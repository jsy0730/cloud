# 저장 규칙

GitHub는 기록용, Google Drive는 큰 파일 보관용으로 나눠 씁니다(2026-10-15부터).

## GitHub(이 저장소)에 커밋하는 것
- 문서: README, CHANGELOG, MANIFEST, 검토 · 점검 기록(.md)
- 스크립트 · 작은 데이터(.py, .js, .json, .csv 등)
- 1MB 이하의 미리보기 이미지(버전 개요 썸네일 등). 더 크면 줄여서 올리거나 Drive로

## Google Drive에 두는 것
- PowerPoint(.pptx), PDF, 1MB가 넘는 렌더 · 사진, 영상 · 압축 파일
- 폴더: `Claude 작업/02_결과물_PPT_보고서/정동관_PPT_버전`
  https://drive.google.com/drive/folders/1WbETMZ26SM-8ikSYZwcrSt9ngCn3Bwbt
- Drive 커넥터는 파일 내용을 호출에 직접 실어야 해서 큰 파일을 올릴 수 없음. Claude는 파일을 채팅 첨부로 전달하고(30MB가 넘으면 사진만 JPEG로 줄인 사본), 사용자가 위 폴더에 올림

## 새 버전을 만들 때
- pptx는 커밋하지 않음(`.gitignore`가 막음). 대신 `jeongdonggwan/pptx/MANIFEST.csv`에 경로 · 크기 · SHA-256과 `where`를 `drive-only`로 기록
- README 버전표와 CHANGELOG에는 내용을 적고, 파일 링크는 위 Drive 폴더로
- 기존에 커밋된 v00~v16 pptx · PDF · 렌더 PNG는 그대로 둠. Git은 지운 파일도 기록에 남기므로 지워도 저장소 용량이 줄지 않음
- 다음 작업의 기준 파일은 `jeongdonggwan/pptx/versions/v16_실별면적표_구체화_25장.pptx`(저장소에 있는 마지막 버전)
