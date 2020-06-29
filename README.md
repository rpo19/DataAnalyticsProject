# DataAnalysisProject

## Installation

### Virtual environment preparation

It is suggested (not mandatory) to use a virtual environment:

* create it
    ```
    # linux
    python3 -m venv /path/to/myenv

    # windows
    python -m venv c:\path\to\myenv
    ```
* activate it
    ```
    # linux
    source /path/to/myenv/bin/activate # bash
    source /path/to/myenv/bin/activate.fish # fish

    # windows
    c:\path\to\myenv\Scripts\activate.bat # cmd
    c:\path\to\myenv\Scripts\Activate.ps1 # powershell
    ```
    look at [Python3 venv](https://docs.python.org/3/library/venv.html) for more.

### Requirements installation
```
pip install -r requirements.txt
```
#### Spacy italian
Run this command (see [https://spacy.io/models/it](https://spacy.io/models/it) for more)
```
python -m spacy download it_core_news_sm
```

N.B: some requirements may need a C++ compiler installed in the machine (e.g. spacy)

## Usage

Activate first the virtual environment if any

### Notebooks

We used `.Rmd` notebook with the help of `jupytext` in order to be able to version them on git

* Run `jupyter notebook`

* Manually open jupyter webapp if needed (probably at [http://localhost:8888/](http://localhost:8888/))

* Open a notebook from `src` folder:

    * `Network.Rmd`: contains network analysis over products

    * `Sentiment.Rmd`: contains sentiment analysis over reviews

### Dash app

* Enter `webapp` folder (e.g. `cd webapp`)

* Run the app:
    ```
    python app.py
    ```

* Go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/). This link is also showed in previous command output
