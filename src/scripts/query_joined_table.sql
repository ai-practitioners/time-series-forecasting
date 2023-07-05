WITH CTE_local_holiday (
	  holiday_date
	, locale
	, locale_name
) AS (
	SELECT DISTINCT
		local_holiday.date
	  , local_holiday.locale
      , local_holiday.locale_name
	FROM holidays_events as local_holiday
	WHERE locale = 'Local' and transferred = 'False'
),

CTE_regional_holiday (
	holiday_date
  , locale
  , locale_name
) AS (
	SELECT DISTINCT
		regional_holiday.date
	  , regional_holiday.locale
	  , regional_holiday.locale_name
	FROM holidays_events as regional_holiday
	WHERE locale = 'Regional' and transferred = 'False'
),

CTE_national_holiday (
	  holiday_date
    , locale
    , locale_name
) AS (
	SELECT DISTINCT
		national_holiday.date
	  , national_holiday.locale
	  , national_holiday.locale_name
	FROM holidays_events as national_holiday
	WHERE locale = 'National' and transferred = 'False'
)

SELECT
	  tr.*
    , str.city
    , str.state
    , str.type
    , str.cluster
    , trans.transactions
    , IF(city_holiday.locale IS NULL, 0, 1) AS is_city_holiday
	, IF(regional_holiday.locale IS NULL, 0, 1) AS is_regional_holiday
    , IF(national_holiday.locale IS NULL, 0, 1) AS is_national_holiday
FROM time_series.train AS tr
LEFT JOIN time_series.stores AS str
	ON tr.store_nbr = str.store_nbr
LEFT JOIN time_series.transactions AS trans
	ON tr.store_nbr = trans.store_nbr AND tr.date = trans.date
LEFT JOIN CTE_local_holiday AS city_holiday
	ON str.city = city_holiday.locale_name AND tr.date = city_holiday.holiday_date
LEFT JOIN CTE_regional_holiday AS regional_holiday
	ON str.city = regional_holiday.locale_name AND tr.date = regional_holiday.holiday_date
LEFT JOIN CTE_national_holiday AS national_holiday
	ON tr.date = national_holiday.holiday_date
;