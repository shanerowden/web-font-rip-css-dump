# google_fonts_rip

I heard that Google was tracking sites and their users through the fonts. So this is just a web bot that I made for fun, having thought of it.


### Install requirements
First make sure you install the requirements with `pip install -r requirements.txt`

### Get a link to rip
Go to fonts dot gaggle dot com and pick the fonts you want to use and when you go to export them, instead of using an import like this in your html...

```
<link href="https://fonts.googleapis.com/css?family=Baloo+Chettan+2&display=swap" rel="stylesheet"> 
```

...you're going to just take that link and pass it to `gfontrip.py` like this:

```
python gfontrip.py "<insert-url>"
```

It's going to download all woff2 files and save them into `static/fonts/`. You're going to find a css file get dumped into `static/css/ripped_google_fonts.css`

Now you're going to put this in your html:
  
```
<link href="static/css/ripped_google_fonts.css" rel="stylesheet">
```

You're going to have to host everything in the `static/` directory locally for it to work...

The script will still try to default on local instances of the fonts and only after grab the URL where you're hosting it.

The code is a little hacky and maybe difficult to read so if you want to improve it feel free.

It's only been tested with fonts I'm using so if it doesn't work let me know.

@shaen@hackers.town
