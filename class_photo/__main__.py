import os
import sys
from dotenv import load_dotenv
from . import bot
from . import face
from . import collage

def get_locations(dir):
    total = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    imgs = []
    for index in range(total):
        imgs.append(f"{dir}/{index}.jpg")
    return imgs

if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) == 2:
        if sys.argv[1] == "--bot":
            bot.main()

        elif sys.argv[1] == "--crop":
            locations = get_locations("img/discord")
            face.crop(locations)

        elif sys.argv[1] == "--collage":
            locations = get_locations("img/cropped")
            collage.make_collage(locations)

        elif sys.argv[1] == "--all":
            bot.main()
            discord_locations = get_locations("img/discord")
            face.crop(discord_locations)
            cropped_locations = get_locations("img/cropped")
            collage.make_collage(cropped_locations)
    else:
        print("Wrong arguments. Consult the README for more information. Only 1 argument at a time.")