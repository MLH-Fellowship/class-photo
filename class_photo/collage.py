from PIL import Image
import math

def make_collage(imgs):
    print("Start creating collage...")
    
    index = len(imgs)
    rows = int(math.sqrt(index))
    cols = math.ceil(index / rows)
    remainder = (rows * cols) - index

    cols_test = cols + 1
    rows_test = math.ceil(index / cols_test)
    remainder_test = (rows_test * cols_test) - index
    
    while remainder_test < remainder:
        cols = cols_test
        rows = rows_test
        remainder = (rows * cols) - index
        cols_test = cols + 1
        rows_test = math.ceil(index / cols_test)
        remainder_test = (rows_test * cols_test) - index

    while (cols * rows) > len(imgs):
        padded_img = Image.new('RGB', (200, 200), (30, 83, 159))
        output_filename = f"img/cropped/{index}.jpg"
        index += 1
        padded_img.seek(0)
        padded_img.save(output_filename)
        imgs.append(output_filename)

    width = 200 * cols
    height = 200 * rows
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
