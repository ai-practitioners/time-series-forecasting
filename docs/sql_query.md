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

:::{admonition} Query explanation
:class: tip

The following query checks for rows and columns per table (views included) within the time_series database. The screenshot following to the code block is the result.
:::

```{code-cell}
SELECT
    rows_table.TABLE_NAME,
    rows_table.TABLE_ROWS,
    columns_sq.TABLE_COLUMNS
FROM INFORMATION_SCHEMA.TABLES AS rows_table
LEFT JOIN (
    SELECT
        table_name,
        COUNT(*) AS TABLE_COLUMNS
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'time_series'
    GROUP BY table_name
) AS columns_sq
ON rows_table.TABLE_NAME = columns_sq.TABLE_NAME
WHERE TABLE_SCHEMA = 'time_series';
```
```{figure} ./docs/img/dataset_rows_columns.png
:height: 150px
:name: All tables rows and columns
```