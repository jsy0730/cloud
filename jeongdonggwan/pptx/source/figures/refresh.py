from PIL import Image, ImageOps, ImageEnhance
import glob, json, os
im = Image.open('img/night_sw.jpg').convert('RGB')
w, h = int(4.7 * 300), int(7.5 * 300)
r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
x = round((im.width - w) * 0.6); im = im.crop((x, 0, x + w, h))
ImageEnhance.Contrast(ImageOps.grayscale(im).convert('RGB')).enhance(1.08).save('img2/concept_grey.jpg', quality=88)
d = {os.path.basename(f): Image.open(f).size for f in glob.glob('img2/*') + glob.glob('img/*')}
json.dump(d, open('dims.json', 'w')); print(d['view_profile.png'], d['shadow_hours.png'])
