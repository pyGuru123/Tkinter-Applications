# Phone Information Scraper

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

It is a simple python tkinter based application to scrape information related to the entered phone number from [find and trace](https://www.findandtrace.com/trace-mobile-number-location) website. The application requires an active internet connection for fetching result. The app scrapes phone information for indian number only.

![Alt text](app.png?raw=true "Phone Information Scraper")

## How to Download

Download this project from here [Download Phone Information Scraper](https://downgit.github.io/#/home?url=https://github.com/pyGuru123/Tkinter-Applications/tree/master/Phone%20Information%20Scraper)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages:
* Mechanize
* Beautifulsoup4

```bash
pip install Mechanize
pip install Beautifulsoup4
```

Mechanize is used to parse data to the search bar and press submit button in the find and trace website, beautifulsoup4 will be used to scrape data from the fetched result.

## Usage

Double click the application.pyw to open the GUI application, then enter the 10 digit valid phone number in the search box and click the search menu to fetch the related information. Don't put +91 or 0 or + in front of the 10 digit phone number


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
