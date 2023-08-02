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

## Motivation of building this query
The final state of the query is built upon the consideration of joining all necessary tables together as a complete table. When queried into working notebook as pandas dataframe, EDA can begin without the need to perform pandas join afterwards. Having a complete or full dataframe to begin with also allows slicing and dicing much easier (i.e. EDA on a particular city or stores).

## The aim for the query final state
Merge as much columns as we can together in the early stage of the project. We will not be needing to jump between database and working space to dig for more data at later phase of analysis. 

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

### Size of tables

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
| train | **3000887 x 6**
| transactions | 83488 x 3

As train table contains the most number of rows, consider it as the fact table and the other tables as dimensions tables.

### Timeline of each cities
Analyzing the length of each cities' timeline can give us a rough idea of how distributed each city time series between each other.

```{code-cell}
SELECT
	MIN(tr.date) AS city_start_date,
  MAX(tr.date) AS city_end_date,
  city
FROM train AS tr
LEFT JOIN stores AS st
  ON tr.store_nbr = st.store_nbr
GROUP BY city;
```

Join `train` and `store` tables with `store_nbr` being the common column. We only join `city` instead of `state` as city is on a more granular level and one column is sufficient for now in this analysis.

![city_timeline](docs/img/city_timeline.png)

Results from this analysis: Each city has the same timeline range from 2013-01-01 to 2017-08-15. But this does not guarantee that all cities will have equal number of time points (observations).