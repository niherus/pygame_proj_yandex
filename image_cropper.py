from PIL import Image

path = 'alien2\\alien.png'
outpath = 'alien2'

img = Image.open(path)
w, h = img.size
CROP_SIZE = 42, 40
N = h // CROP_SIZE[1]

for i in range(N):
    pic = img.crop((0, 40 * i, 42, 40 * (i + 1)))
    pic.save(f'{outpath}\\{N - 1 - i}.png')

