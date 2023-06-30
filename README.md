# Time Series Forecasting

This repository is created mainly to pick up, build and enhance your concepts and knowledge surrounding time series forecasting problem statements or project.

Anyone is free to participate in the contribution to this repository. The idea is also to learn and network from one another as well.

# Data Set

The data set chosen for this repository comes from Kaggle. Click here for the link to download the [M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data) data set.

You should find 5 csv files when you clicked into the link above. As the total file sizes added up to around 0.5GB I would recommend you to create a folder called `data` in the root directory of this repository and put the csv files in.


```
├── data
│    ├── calendar.csv
│    ├── sales_train_evaluation.csv
│    ├── sales_train_validation.csv
│    ├── sample_submission.csv
│    ├── sell_prices.csv
├── README.md
├── src
│   ├── ...
│   ├── ...
└── .gitignore
```
The initial intention was to ingest the csv files into your preferred RDBMS and query the data thereafter, but it seems `sales_train_evaluation.csv`, `sales_train_validation` have too much columns (~1900) for DB to handle. If anyone found a better way please share!