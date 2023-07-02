# Time Series Forecasting

This repository is created mainly to pick up, build and enhance your concepts and knowledge surrounding time series forecasting problem statements or project.

Anyone is free to participate in the contribution to this repository. The idea is also to learn and network from one another as well.

# Data Set

The data set chosen for this repository comes from Kaggle. Click here for the link to download the [Store Sales - Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data?select=oil.csv) data set.

You should find 7 csv files when you clicked into the link above. I would recommend you to create a folder called `data/raw/` in the root directory of this repository and put the csv files in.

```
├── data
│    └── raw
│         ├── holiday_events.csv
│         ├── oil.csv
│         ├── sample_submission.csv
│         ├── stores.csv
│         ├── test.csv
│         ├── train.csv
│         ├── transactions.csv
├── README.md
├── src
│   ├── ...
│   ├── ...
└── .gitignore
```

The intention is to ingest the csv files into your preferred RDBMS and query the data thereafter.

The inital data set recommneded for this repository was the [M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data) data set. We decided to switch to this smaller data set as some of us had troubles bringing the data set into our working space. If anyone has a solution to this, we welcome you to join us in our conversation tracked in [this commit](https://github.com/ai-practitioners/time-series-forecasting/commit/e542144dfe6fce26b657393c287a6c3dd85b11ea) and [issue #3](https://github.com/ai-practitioners/time-series-forecasting/issues/3). 