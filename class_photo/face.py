import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

def crop(imgs):
    try:
        os.mkdir("img/cropped")
        print("Created cropped directory!")
    except FileExistsError:
        print("cropped directory already exists! Overwriting existing photos.")

    print("Cropping...")
    img_filenames = []
    for index, img in enumerate(imgs):
        with open(f"img/discord/{index}.jpg", 'rb') as image:
            faces = detect_face(image)
            output_filename = f"img/cropped/{index}.jpg"
            img_filenames.append(output_filename)
            image.seek(0)
            try:
                crop_faces(image, faces, output_filename)
            except:
                im = Image.open(image)
                im.save(output_filename)

def detect_face(face_file, max_results=1):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(
        image=image, max_results=max_results).face_annotations

def crop_faces(image, faces, output_filename):
    im = Image.open(image)

    im_width = im.size[0]
    im_height = im.size[1]

    left = 0
    right = 0
    top = 0
    bottom = 0

    for face in faces:
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        
    centre = int((box[0][0] + box[1][0])/2)
    middle = int((box[0][1] + box[2][1])/2)
    width = abs(box[1][0] - box[0][0]) + (0.1 * im_width)
    height = abs(box[2][1] - box [0][1]) + (0.1 * im_height)

    if (max(width, height) < im_width) & (max(width, height) < im_height):
        distance = int(max(width, height)/2)
    elif (min(width, height) < im_width) & (min(width, height) < im_height):
        distance = int(min(width, height)/2)
    else:
        distance = int(min(im_width, im_height)/2)
    
    left = centre - distance
    right = centre + distance
    top = middle - distance
    bottom = middle + distance

    if left < 0:
        right -= left
        left = 0
    
    if right > im_width:
        left -= (right - im_width)
        right = im_width
    
    if top < 0:
        bottom -= top
        top = 0
    
    if bottom > im_height:
        top -= (bottom - im_height)
        bottom = im_height

    box2 = (left,top,right,bottom)
    new_im = im.crop(box2)
    new_im = new_im.resize((200,200), Image.ANTIALIAS)
    new_im.save(output_filename)
