select
	tr.`date`, tr.family, sum(tr.sales), sum(tr.onpromotion), 
	tr.store_nbr, st.city,
	YEAR(tr.`date`) `year`,
    MONTH(tr.`date`) `month`,
    DAY(tr.`date`) `day_of_month`,
	sum(transactions)
from
	train as tr
left join stores as st
    on tr.store_nbr = st.store_nbr
left join transactions txn 
    on tr.`date` = txn.`date` AND tr.store_nbr = txn.store_nbr
where
 	year(tr.`date`) between 2013 and 2015
group by tr.`date`, tr.family, st.city, tr.store_nbr
having st.city = 'Quito'
order by tr.`date`