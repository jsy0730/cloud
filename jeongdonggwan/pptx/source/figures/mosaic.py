import sys
from PIL import Image
groups = [[2,4,5,9],[10,11,12,13],[15,17,18,19],[20,21,3,14]]
for gi, g in enumerate(groups):
    S = Image.new('RGB', (1500, 850), (120,120,120))
    for k, p in enumerate(g):
        im = Image.open(f'out2/p{p:02d}.png').resize((740, 416))
        S.paste(im, ((k % 2) * 760, (k // 2) * 430))
    S.save(f'out2/m{gi+1}.png')
