# SaveFromYT

SaveFromYT is a simple python tkinter based application to download mp4 videos and mp3 audio from a youtube video url

![Alt text](app.png?raw=true "SaveFromYT")

The application requires an active internet connection for downloading mp4/mp3.

## How to Download

Download this project from here [Download SaveFromYT](https://downgit.github.io/#/home?url=https:%2F%2Fgithub.com%2FpyGuru123%2FTkinter-Applications%2Ftree%2Fmaster%2FYoutube%20-%20AudioVideo%20Downloader)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :-
* pafy
* youtube-dl

```bash
pip install pafy
pip install youtube-dl
```

pafy uses youtube-dl as backend, so remember to install both packages

#### API Note

Pafy comes with default api key, but if you get API limit exceede error, get yourself an youtube v3 api key from [google console](https://developers.google.com/youtube/v3/getting-started) and paste in the script beginning

```bash
pafy.set_api_key(key)
```

## Usage

Double click the application.pyw to open the GUI application, then paste the youtube video url which you want download and click enter, the followup screen will come up with video metadata and download buttons for downloading files. You can choose video quality from the option box before downloding.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.