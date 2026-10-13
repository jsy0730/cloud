import os,glob,sys
from PIL import Image,ImageDraw
R=os.environ['TEMP'].replace(chr(92),'/')+'/cloud_repo/jeongdonggwan/'
def sheet(files,out,cols=5,tw=360,th=240):
    rows=(len(files)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*(th+22)),'white'); d=ImageDraw.Draw(S)
    for i,f in enumerate(files):
        try:
            im=Image.open(f).convert('RGB'); sz=im.size; im.thumbnail((tw-6,th-6))
            x=(i%cols)*tw; y=(i//cols)*(th+22)
            S.paste(im,(x+3,y+3)); d.text((x+4,y+th+4),os.path.relpath(f,R)[-40:]+f' {sz}',fill='black')
        except Exception as e: print(f,e)
    S.save(out)
sheet(sorted(glob.glob(R+'build/assets/*')),'s_assets.jpg')
sheet(sorted(glob.glob(R+'build/final/*'))+sorted(glob.glob(R+'build/section/*_new.png'))+[R+'build/env_map.png',R+'build/iso.png',R+'build/transit_map.png'],'s_final.jpg')
sheet(sorted(glob.glob(R+'research/photos*/*')),'s_photos.jpg')
sheet(sorted(glob.glob(R+'research/data/cand/*'))+sorted(glob.glob(R+'research/data/contact_*')),'s_cand.jpg',cols=6)
