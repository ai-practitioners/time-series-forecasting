---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Documentation and Reasoning for SQL Query

This page documents the thought and reasoning process of arriving at the final state of the query to be used in the dataset analysis for this project.

## About the setup

Workstation: MacOS 13 (arm64)<br>
Software: MySQL Community Server - GPL (8.0.33)<br>
Environment: localhost

## About the database and dataset

The 5 main files used in our analysis are the following csv files which are locally uploaded using MySQL Workbench. Therein these csv files are located in `time_series` database. We also use the file names as name of individual tables and simple abbreviations in our query to be straightforward.


| File name | Table name (In database) | Table name (In query)
| :--- | :--- | :---
| holiday_events.csv | holiday_events | `hols`
| oil.csv | oil | `o`
| stores.csv | stores | `st`
| train.csv | train | `tr`
| transactions.csv | transactions | `txn`

## More about the dataset

Let's first take a quick look at the size of tables.

```{code-cell}
-- Replace table name to check size of each table
SELECT COUNT(*)
FROM holidays_events;

SELECT COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'time_series' AND table_name = 'holidays_events';
```

| Table name (In database) | Rows x Columns
| :--- | :---
| holiday_events | 350 x 6
| oil | 1218 x 2
| stores | 54 x 5
| train | 3000887 x 6
| transactions | 83488 x 3

As train table contains the most number of rows, consider it as the main table for the rest of the analysis.