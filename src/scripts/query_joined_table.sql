WITH CTE_local_holiday (
	  date
    , locale
    , locale_name
) AS (
	SELECT
		local_holiday.date
      , local_holiday.locale
      , local_holiday.locale_name
	FROM holidays_events as local_holiday
	WHERE locale = 'local' and transferred = 'False'
)

SELECT
	  tr.*
    , str.city
    , str.state
    , str.type
    , str.cluster
    , trans.transactions
    , local_holiday.locale -- make this column become 1 if join is ok, else null. rename column to is_locale_holiday 
FROM time_series.train AS tr
LEFT JOIN time_series.stores AS str
	ON tr.store_nbr = str.store_nbr
LEFT JOIN time_series.transactions AS trans
	ON tr.store_nbr = trans.store_nbr AND tr.date = trans.date
LEFT JOIN CTE_local_holiday AS local_holiday
	ON str.city = local_holiday.locale_name AND tr.date = local_holiday.date
WHERE tr.date = '2013-03-02' AND str.city = 'Manta'
;