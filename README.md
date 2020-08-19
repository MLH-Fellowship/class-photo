# Class Photo
📷 Discord Bot that downloads and crops photos around everyone's face

## Setup

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Fill out `.env` with the fields in `example.env`.

## Run

There's 3 stages:
1. Download photos from Discord
2. Crop them
3. Make collage

For downloading only
```
python -m class_photo --bot
```

For cropping only
```
python -m class_photo --crop
```

For collage only
```
python -m class_photo --collage
```

For everything
```
python -m class_photo --all
```
