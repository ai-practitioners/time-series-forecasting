USE time_series;

CREATE OR REPLACE VIEW full_df AS

WITH CityHolidays AS (
  SELECT
    date,
    locale_name,
    GROUP_CONCAT(DISTINCT type) AS type
  FROM holidays_events
  WHERE type != 'Work Day' AND locale = 'Local' AND transferred = 'False' AND date BETWEEN '2013-01-01' AND '2017-08-15'
  GROUP BY date, locale_name
),

StateHolidays AS (
  SELECT
    date,
    locale_name,
    type
  FROM holidays_events
  WHERE type != 'Work Day' and locale = 'Regional' and transferred = 'False' AND date BETWEEN '2013-01-01' AND '2017-08-15'
  GROUP BY date, locale_name, type
  ),
  
NationHolidays AS (
  SELECT
    date,
    locale_name,
    type
  FROM (
    SELECT
      date,
      locale_name,
      type,
      ROW_NUMBER() OVER(PARTITION BY date ORDER BY locale_name, type) AS rn
    FROM holidays_events
    WHERE type != 'Work Day' AND locale = 'National' AND transferred = 'False' AND date BETWEEN '2013-01-01' AND '2017-08-15'
  ) AS RankedHolidays
  WHERE rn = 1
)
  
SELECT
  tr.*,
  st.city,
  st.state,
  c_hols.type AS city_hols_type,
  IF(c_hols.type IS NULL, 'No', 'Yes') as city_hols,
  s_hols.type AS state_hols_type,
  IF(s_hols.type IS NULL, 'No', 'Yes') as state_hols,
  n_hols.type AS nation_hols_type,
  IF(n_hols.type IS NULL, 'No', 'Yes') as nation_hols,
  o.dcoilwtico AS oil_price,
  st.type,
  st.cluster,
  txn.transactions
FROM train AS tr
LEFT JOIN stores AS st
  ON tr.store_nbr = st.store_nbr
LEFT JOIN CityHolidays AS c_hols
  ON tr.date = c_hols.date AND st.city = c_hols.locale_name
LEFT JOIN StateHolidays AS s_hols
  ON tr.date = s_hols.date AND st.state = s_hols.locale_name
LEFT JOIN NationHolidays AS n_hols
  ON tr.date = n_hols.date
LEFT JOIN oil as o
  ON tr.date = o.date
LEFT JOIN transactions AS txn
  ON tr.date = txn.date AND tr.store_nbr = txn.store_nbr
ORDER BY id
;
