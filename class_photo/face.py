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
        with open(f"img/discord/{img[1]}.jpg", 'rb') as image:
            faces = detect_face(image)
            output_filename = f"img/cropped/{index}.jpg"
            img_filenames.append(output_filename)
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
    left = 0
    bottom = 0
    width = 0
    height = 0
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        width = abs(box[1][0] - box[0][0]) + 50
        height = abs(box[2][1] - box [0][1]) + 50
        diff = abs(width - height)
        if width >= height:
            height = width + 50
        else:
            width = height + 50

        left = box[0][0] - 50
        bottom = box[0][1] + 50

    box2 = (left,bottom,left+width,bottom+height+50)
    new_im = im.crop(box2)
    new_im = new_im.resize((1000,1000), Image.ANTIALIAS)
    new_im.save(output_filename)
