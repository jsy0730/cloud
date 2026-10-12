import sys, json
from PIL import Image
deck = sys.argv[1]; D = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/decks/'
order = json.load(open(D + f'{deck}/project/deck.json'))['order']
n = 4
for k in range(0, len(order), n):
    sheet = Image.new('RGB', (1920, 1080), 'white')
    for i, sid in enumerate(order[k:k + n]):
        im = Image.open(D + f'{deck}/preview/{sid}.png').convert('RGB').resize((960, 540), Image.LANCZOS)
        sheet.paste(im, ((i % 2) * 960, (i // 2) * 540))
    sheet.save(D + f'{deck}/preview/sheet_{k // n + 1}.png')
print((len(order) + n - 1) // n)
