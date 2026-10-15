import sys, zipfile, re, shutil
# Korean word-wrap needs lang="ko-KR" on every run (en-US makes PowerPoint break Korean mid-word)
src = sys.argv[1]; tmp = src + '.tmp'
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
cnt = 0
for it in zin.infolist():
    data = zin.read(it.filename)
    if re.match(r'ppt/(slides/slide|charts/chart)\d+\.xml$', it.filename):
        x = data.decode('utf8')
        n = x.count('lang="en-US"')
        cnt += n
        x = x.replace('lang="en-US"', 'lang="ko-KR" altLang="en-US"')
        data = x.encode('utf8')
    zout.writestr(it, data)
zout.close(); zin.close()
shutil.move(tmp, src)
print('lang runs set to ko-KR:', cnt)
