from PIL import Image
import math
import os

def make_collage(imgs):
    print("Start creating collage...")
    
    length = len(imgs)
    index = length - 1
    rows = int(math.sqrt(length))
    cols = math.ceil(length / rows)
    remainder = (rows * cols) - length

    cols_test = cols + 1
    rows_test = math.ceil(length / cols_test)
    remainder_test = (rows_test * cols_test) - length

    while remainder_test < remainder:
        cols = cols_test
        rows = rows_test
        remainder = (rows * cols) - length
        cols_test = cols + 1
        rows_test = math.ceil(length / cols_test)
        remainder_test = (rows_test * cols_test) - length

    # Add padding photos
    padding_start = len(imgs) - 1
    while (cols * rows) > len(imgs):
        padded_img = Image.new('RGB', (200, 200), (30, 83, 159))
        output_filename = f"img/cropped/{index}.jpg"
        index += 1
        padded_img.seek(0)
        padded_img.save(output_filename)
        imgs.append(output_filename)
    
    cols = int(os.getenv("COLUMNS"))
    rows = int(os.getenv("ROWS"))
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

    # delete padding
    padding_imgs = len(imgs) - padding_start - 1
    print(padding_imgs)
    for filename_index in range(padding_imgs):
        print(filename_index)
        print(padding_start)
        os.remove(f"img/cropped/{padding_start + filename_index}.jpg")
