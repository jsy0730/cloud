from PIL import Image
groups = {'a': [1, 2, 3, 4], 'b': [14, 15, 16, 17], 'c': [18, 19, 20, 21]}
for k, g in groups.items():
    S = Image.new('RGB', (1500, 850), (120, 120, 120))
    for i, p in enumerate(g):
        S.paste(Image.open(f'out2/p{p:02d}.png').resize((740, 416)), ((i % 2) * 760, (i // 2) * 430))
    S.save(f'out2/n_{k}.png')
