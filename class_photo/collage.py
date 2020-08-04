from PIL import Image

def make_collage(imgs):
    print("Start creating collage...")
    width = 1920
    height = 1080
    # work out based on number of images
    cols = 6
    rows = 4

    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_image = Image.new('RGB', (width, height))
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
            print(i, x ,y)
            new_image.paste(images[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_image.save("img/collage.jpg")