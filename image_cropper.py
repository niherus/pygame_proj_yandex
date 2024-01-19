from PIL import Image

path = 'images\\boss\\turtle.png'
outpath = 'images\\boss\\'

img = Image.open(path)
w, h = img.size
CROP_SIZE = 70, 58
N = h // CROP_SIZE[1]

for i in range(N):
    pic = img.crop((0, CROP_SIZE[1] * i, CROP_SIZE[0], CROP_SIZE[1] * (i + 1)))
    pic.save(f'{outpath}\\{N - 1 - i}.png')

