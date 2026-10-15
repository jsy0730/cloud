import sys, zipfile, re, shutil, os
src = sys.argv[1]; tmp = src + '.tmp'
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
cnt = 0
for it in zin.infolist():
    data = zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$', it.filename):
        x = data.decode('utf8')
        def add_attr(m):
            global cnt
            tag = m.group(0)
            if 'eaLnBrk=' in tag: return tag
            cnt += 1
            return tag.replace('<a:pPr', '<a:pPr eaLnBrk="0"', 1)
        x = re.sub(r'<a:pPr(?=[\s/>])[^>]*>', add_attr, x)
        # paragraphs without pPr
        def para(m):
            global cnt
            cnt += 1
            return '<a:p><a:pPr eaLnBrk="0"/>'
        x = re.sub(r'<a:p>(?!<a:pPr)', para, x)
        data = x.encode('utf8')
    zout.writestr(it, data)
zout.close(); zin.close()
shutil.move(tmp, src)
print('nobreak paragraphs:', cnt)
