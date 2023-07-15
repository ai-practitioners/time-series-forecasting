# Time Series Forecasting - Motivation
This repository is created to mainly pick up, build and enhance concepts and knowledge surrounding time series forecasting problem statements or projects.

Anyone is free to participate in the contribution to this repository. The idea is also to learn and network with one another as well.

Also, the second purpose is to get used to tools that allow collaboration between contributors. An example of such tools is DVC where data versioning, model experiment, CI/CD, etc. is allowed.

# About Dataset
The data set chosen for this repository comes from Kaggle. Click here for the link to download the [Store Sales - Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data?select=oil.csv) data set.

You should find 7 CSV files when you clicked on the link above. I would recommend you create a folder called `data/raw/` in the root of your project directory and put the CSV files in.

```
.
├── ...
├── data
│   └── raw
│       ├── holiday_events.csv
│       ├── oil.csv
│       ├── sample_submission.csv
│       ├── stores.csv
│       ├── test.csv
│       ├── train.csv
│       └── transactions.csv
└── ...
```

The intention is to ingest the CSV files into your preferred RDBMS and query the data thereafter.
The initial data set recommended for this repository was the [M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data) data set. We decided to switch to this smaller data set as some of us had trouble bringing the data set into our working space due to workspace limitations. If anyone has a solution to this, we welcome you to join us in our conversation tracked in [this commit](https://github.com/ai-practitioners/time-series-forecasting/commit/e542144dfe6fce26b657393c287a6c3dd85b11ea) and [issue #3](https://github.com/ai-practitioners/time-series-forecasting/issues/3).

# Getting Started and Setup
To ensure all contributors are working in a similar setup, you may follow the following steps to replicate the initial setup of this repository.

**Clone the project into your preferred location in your local directory.**

```bash
  git clone https://github.com/ai-practitioners/time-series-forecasting.git
```

**Go to the project directory.**

```bash
  cd time-series-forecasting
```

**Install `virtualenv`.**

```bash
  # install virtualenv using pip
  pip install virtualenv
```

**Create a virtual environment with a Python version of your choice.**

This repository uses `python3.9.13`. For simplicity, we use `venv` as the name of the virtual environment in this setup instructions. You can use any name of your choice by replacing the word "venv".

```bash
  virtualenv venv -p <python-version>
```

**Activate your virtual environment.**

```bash
# if your workstation is running on Windows OS
source venv/Scripts/activate

# if your workstation is running on Mac OS
source venv/bin/activate
```
To deactivate the virtual environment, simply `deactivate` it.
```bash
deactivate
```

**Ensure that venv is selected.**

After the following command is entered in terminal, you should expect to see the path of python being python of your virtual environment.

```bash
# Windows OS
where python
</path/to/venv/Scripts/python>

# Mac OS
which python
</path/to/venv/bin/python>
```

**Add packages into virtual environment.**

After activating your virtual environment, you can add libraries to it by using `pip`. Ensure you are in the same directory as your virtual environment, execute the following command in the terminal and wait for the installations to complete. 
```bash
pip install -r requirements.txt
```