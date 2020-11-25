import discord
from discord.ext import commands
import os
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
from . import face

bot = commands.Bot('-cp')

def main():
    bot.run(os.getenv("TOKEN"))

@bot.event
async def on_ready():
    print('Bot Online!')
    await get_photos()
    await bot.logout()

async def get_photos():   
    photo_messages = await get_all_photo_messages()
    print(f"Collected {len(urls)} photo urls in total")
    
    try:
        os.mkdir("img")
        print("Created img directory!")
    except FileExistsError:
        print("img directory already exists!")

    try:
        os.mkdir("img/discord")
        print("Created discord directory!")
    except FileExistsError:
        print("discord directory already exists! Overwriting existing photos.")

    # Save only the latest photo from each user
    users = {}
    for message in photo_messages:
        users[message.author] = message.attachments[0].url

    for index, url in enumerate(users.values()):
        await save_photo(index, url)

    print(f"Saved all {len(urls)} photos!")

async def get_all_photo_messages():
    photo_messages = []
    selfie_channel = bot.get_channel(int(os.getenv("CHANNEL")))
    all_messages = await selfie_channel.history(limit=1000).flatten()

    for message in all_messages:
        if len(message.attachments) > 0:
            photo_messages.append(message)
    return photo_messages

async def save_photo(index, url):
    try:
        response = requests.get(url[0], timeout=5)
        try:
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image = rotate_if_exif_specifies(image)
            image.convert('RGB').save(f"img/discord/{index}.jpg", optimize=True)

        except requests.HTTPError:
            print('HTTP error')

    except requests.exceptions.ConnectionError:
        print('Network error')

def rotate_if_exif_specifies(image):
    try:
        exif_tags = image._getexif()
        if exif_tags is None:
            # No EXIF tags, so we don't need to rotate
            return image

        value = exif_tags[274]
    except KeyError:
        # No rotation tag present, so we don't need to rotate
        print('EXIF data present but no rotation tag, so not transforming')
        return image

    value_to_transform = {
        1: (0, False),
        2: (0, True),
        3: (180, False),
        4: (180, True),
        5: (-90, True),
        6: (-90, False),
        7: (90, True),
        8: (90, False)
    }

    try:
        angle, flip = value_to_transform[value]
    except KeyError:
        print(f'EXIF rotation \'{value}\' unknown, not transforming')
        return image

    if angle != 0:
        image = image.rotate(angle)

    if flip:
        image = image.tranpose(Image.FLIP_LEFT_RIGHT)

    return image
