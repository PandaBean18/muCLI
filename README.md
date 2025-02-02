# muCLI

**muCLI** is a command line program to play music that uses the youtube and spotify api to play songs along with its lyrics
[image](./demoImg.png)

## API credentials

The application uses both spotify and youtube credentials. You can get spotify client id and client secret by creating a new app on spotify developer console, and the youtube client id and client secret by creating a new GCP project that has youtube api enabled.
The credentials need to be stored in a .env file in such manner:

```txt
client_secret=<youtube_client_secret>
client_id=<youtube_client_id>
SPOTIPY_CLIENT_ID=<spotify_client_id>
SPOTIPY_CLIENT_SECRET=<spotify_client_secret>
```

**Note**: it IS spotipy in the variable names, not spotify, program uses the spotipy library and I copied the variable names straight from the documentation and was too lazy to change them.

## System requirements

[yt-dlp](https://github.com/yt-dlp/yt-dlp#readme)
[ytmusicapi](https://ytmusicapi.readthedocs.io/en/stable/)
[spotipy](https://spotipy.readthedocs.io/en/2.25.0/)
[syrics](https://github.com/akashrchandran/syrics)
pydub
numpy
mpg321

## Lyrics

The application uses syrics to get the lyrics, you will need to set it up and can check how to set it up [here](https://github.com/akashrchandran/syrics). As he has mentioned, getting lyrics from spotify maybe against their TOS, this example here is for educational purposes only.
