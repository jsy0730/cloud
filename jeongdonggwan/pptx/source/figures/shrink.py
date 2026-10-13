import glob, re
from PIL import Image
fs = sorted(glob.glob('out2/*.PNG'), key=lambda f: int(re.findall(r'(\d+)\.PNG', f)[0]))
for i, f in enumerate(fs, 1): Image.open(f).convert('RGB').resize((1440, 810)).save(f'out2/p{i:02d}.png')
print(len(fs))
