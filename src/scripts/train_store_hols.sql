select
	id, tr.family, tr.sales, tr.onpromotion, 
	city, state, cluster, 
	locale, locale_name, description, transferred,
	st.`type`, hols.`type` hol_type, 
	tr.store_nbr,
	tr.`date` 
from
	train as tr
left join stores as st
on
	tr.store_nbr = st.store_nbr
left join holidays_events hols 
on tr.`date` = hols.`date`
where
	year(tr.`date`) between 2013 and 2015
-- constraint where rowcount (1,972,674)
-- no constraint, full rowcount (3,054,348)
