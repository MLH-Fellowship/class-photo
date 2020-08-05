from PIL import Image
import math

def make_collage(imgs):
    print("Start creating collage...")
    
    rows = int(math.sqrt(len(imgs)))
    cols = math.ceil(len(imgs) / rows)
    index = len(imgs)
    while (cols * rows) > len(imgs):
        padded_img = Image.new('RGB', (910, 512), (30, 83, 159))
        index += 1
        output_filename = f"img/cropped/{index}.jpg"
        padded_img.seek(0)
        padded_img.save(output_filename)
        imgs.append(output_filename)

    width = 1000 * cols
    height = 1000 * rows
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_image = Image.new('RGB', (width, height), (30, 83, 159))
    images = []
    for p in imgs:
        im = Image.open(p)
        im.thumbnail(size)
        images.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            new_image.paste(images[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_image.save("img/collage.jpg")