import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from . import collage

def crop(imgs):
    try:
        os.mkdir("img/cropped")
    except FileExistsError:
        pass        
    print("Cropping...")
    img_filenames = []
    for index, img in enumerate(imgs):
        print(img)
        with open(f"img/discord/{img[1]}.jpg", 'rb') as image:
            faces = detect_face(image)
            print(f"Found {len(faces)} face{'' if len(faces) == 1 else 's'}")
            output_filename = f"img/cropped/{index}.jpg"
            img_filenames.append(output_filename)
            print(f'Writing to file {output_filename}')
            image.seek(0)
            highlight_faces(image, faces, output_filename)

    collage.make_collage(img_filenames)

def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(
        image=image, max_results=max_results).face_annotations

def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    left = 0
    top = 0
    right = 0
    bottom = 0
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        width = abs(box[1][0] - box[0][0]) + 50
        height = abs(box[2][1] - box [0][1]) + 50
        diff = abs(width - height)
        print(f"Box: {box}")
        print(f"Width: {width}")
        print(f"Height: {height}")
        print(f"Difference: {diff}")
        if width >= height:
            height = width + 50
        else:
            width = height + 50

        left = box[0][0] - 50
        bottom = box[0][1] + 50

    box2 = (left,bottom,left+width,bottom+height+50)
    im2 = im.crop(box2)
    im2.save(output_filename)
