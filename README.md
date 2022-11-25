# Class Photo
📷 Discord Bot that downloads and crops photos around everyone's face

## Setup

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Fill out `.env` with the fields in `example.env`.

Make sure you have a service account for using the Google Cloud Vision API. Instructions [here](https://cloud.google.com/vision/docs/libraries#client-libraries-install-python).

## Run

There's 3 stages:
1. Download photos from Discord
2. Crop them
3. Make collage

For downloading only
```
python -m class_photo --discord
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
