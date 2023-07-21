USE time_series;

CREATE OR REPLACE VIEW train_store_hols AS
select
	id, tr.family, tr.sales, tr.onpromotion, 
	city, state, cluster, 
	locale, locale_name, description, transferred,
	st.`type`, hols.`type` hol_type, 
	tr.store_nbr,
	tr.`date`, 
	YEAR(tr.`date`) `year`,
    MONTH(tr.`date`) `month`,
    DAY(tr.`date`) `day_of_month`,
	sum(transactions)
from
	train as tr
left join stores as st
    on tr.store_nbr = st.store_nbr
left join holidays_events hols 
    on tr.`date` = hols.`date`
left join transactions txn 
    on tr.`date` = txn.`date` AND tr.store_nbr = txn.store_nbr
where
    year(tr.`date`) between 2013 and 2015
-- constraint where rowcount (1,972,674)
-- no constraint, full rowcount (3,054,348)
