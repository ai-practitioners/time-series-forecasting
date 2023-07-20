CREATE OR REPLACE VIEW quito AS
select
    -- count(*)
	tr.`date`, tr.family, 
	tr.store_nbr, 
	YEAR(tr.`date`) `year`,
    MONTH(tr.`date`) `month`,
    DAY(tr.`date`) `day_of_month`,
	COALESCE(SUM(onpromotion),0) as onpromotion_sum,
    COALESCE(SUM(transactions),0) as transactions_sum,
    COALESCE(SUM(sales),0) as sales_sum
from
	train as tr
left join stores as st
    on tr.store_nbr = st.store_nbr
left join transactions txn 
    on tr.`date` = txn.`date` AND tr.store_nbr = txn.store_nbr
where
 	-- year(tr.`date`) = 2013
    st.city = 'Quito'
    -- and tr.store_nbr = 44
group by tr.`date`, tr.family, tr.store_nbr
order by tr.`date`
