from PIL import Image

path = 'croko\\croko.png'
outpath = 'croko'

img = Image.open(path)
w, h = img.size
CROP_SIZE = 90, 28
N = h // CROP_SIZE[1]

for i in range(N):
    pic = img.crop((0, CROP_SIZE[1] * i, CROP_SIZE[0], CROP_SIZE[1] * (i + 1)))
    pic.save(f'{outpath}\\{N - 1 - i}.png')

