import sys,glob,os
from PIL import Image,ImageDraw
def sheet(files,out,cols=6,tw=330,th=230):
    rows=(len(files)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*(th+20)),'white'); d=ImageDraw.Draw(S)
    for i,f in enumerate(files):
        try:
            im=Image.open(f).convert('RGB'); sz=im.size; im.thumbnail((tw-6,th-6))
            x=(i%cols)*tw; y=(i//cols)*(th+20); S.paste(im,(x+3,y+3)); d.text((x+4,y+th+3),os.path.basename(f)+f' {sz}',fill='black')
        except Exception as e: print(f,e)
    S.save(out)
pat=sys.argv[1]; sheet(sorted(glob.glob(pat)),sys.argv[2])
