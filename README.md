# Metal Subgenre Pairing Analyses

## Description and Usage 

1. [scraper.py](scraper.py) scrapes [Encyclopaedia Metallum](https://www.metal-archives.com/browse/genre) for metal bands by genre, then creates and adds data to the SQLite database [metallum_bands.db](metallum_bands.db) and .csv file [metallum_bands.csv](data/metallum_bands.csv). The file [scraper.qmd](scraper.qmd) represents a Quarto-enabled version of this file. 

2. [sql_subgenre_cleaning.qmd](sql_subgenre_cleaning.qmd) parses the `genre` field in the data with SQLite code to represent each band by its component subgenres. 

3. [subgenre pairings.qmd](subgenre_pairings.qmd) analyzes the associations between subgenres through market basket analysis techniques (i.e., support, confidence, and lift) using the [arules](https://github.com/mhahsler/arules) package in R. The resulting processed data is available following analysis as [sub_metal_bands.csv](sub_metal_bands.csv).

4. The main findings from [subgenre_pairings.qmd](subgenre_pairings.qmd) are also summarized in the file [tableau_dash.qmd](tableau_dash.qmd).

## Libraries Used and Requirements

For integration of Python, R, and SQLite code, Quarto markdown (.qmd) files under Quarto version 1.3.450 were created in this project. 

The [scraper.py](scraper.py) file utilizes Python version 3.12.2 and the libraries listed in [py_requirements.txt](py_requirements.txt). 

Additionally, [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) must be installed and enabled to run the web scraping file. 

Files [sql_subgenre_cleaning.qmd](sql_subgenre_cleaning.qmd) and [subgenre_pairings.qmd](subgenre_pairings.qmd) used R version 4.4.1 and the packages listed in [r_requirements.txt](r_requirements.txt).

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE) for more information).

## Acknowledgements

With this being my first try at web scraping, I greatly benefitted from viewing Bright Data's tutorial on [Web Scraping With Python](https://brightdata.com/blog/how-tos/web-scraping-with-python) 
and their [Guide to Web Scraping With Selenium in 2024](https://brightdata.com/blog/how-tos/using-selenium-for-web-scraping).

The [arules](https://github.com/mhahsler/arules) package in R is an excellent package that provided me with everything I needed to mine item associations using market basket analysis metrics. Additionally, Michael Hahsler's [textbook](https://mhahsler.github.io/Introduction_to_Data_Mining_R_Examples/book/index.html) provides helpful [code examples](https://mhahsler.github.io/Introduction_to_Data_Mining_R_Examples/book/association-analysis-basic-concepts-and-algorithms.html) for using the `arules` package.

Remedying the complexity of visualizing item-level associations in Tableau, I found [Do Mo(o)re With Data](https://domoorewithdata.com/)'s post on [market basket analysis](https://domoorewithdata.com/2023/07/19/it-depends-market-basket-analysis/) to be incredibly helpful. 

Lastly, these analyses would not be possible without the hard work and dedication of those at [Encyclopaedia Metallum](https://www.metal-archives.com/). Their entire website is organized and documented incredibly well, and I am grateful that they permit web scraping of band data. 