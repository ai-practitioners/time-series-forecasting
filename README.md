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

# Database and Environment Variables
This repository has its way of setting up a database for learners to extract the data set. The following steps attempt to mimic how enterprises store data. However, for this learning project, we try to develop our data pipeline architecture in a way that is zero cost yet not compromising project collaborations.

We established some principles for the architecture:
 - Single source of truth.
 - Data versioning.
 - Replicability. 

The tools needed to set up the database follows the table below. You will need to have a [Google account](https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp) for this setup.
| Tool | Purpose |
| :--- | :--- |
| [MySQL Workbench Community Server](https://www.mysql.com/) | Collaborator's local database |
| [Data Version Control](https://dvc.org/) | Data versioning |
| [Google Drive](https://www.google.com/intl/en_sg/drive/) | Cloud storage of meta files for usage with DVC |

**Local database setup using MySQL Workbench**

1. [Install MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-installing.html) if you have not done so. You will be required to set a password during the installation. Please have this password recorded or saved as you will need it later.
2. Launch MySQL Workbench and [create a new schema (database)](https://dev.mysql.com/doc/workbench/en/workbench-faq.html#faq-workbench-create-database). In this learning project, the name of the database is `time_series`.
3. Now, our database needs tables. These tables and their data come from the 7 CSV files from Kaggle. Using [Table Data Import Wizard](https://dev.mysql.com/doc/workbench/en/wb-admin-export-import-table.html), upload all the CSV files. `train.csv` contains more than 3 million rows, so using the wizard will not be efficient. This learning repository provides a script to programmatically import `train.csv` into `time_series` database. The script can be found at this location of the repository `src/scripts/import_csv_to_local_db.sql`. Run the script on a new query tab.
