CREATE OR REPLACE VIEW sales_year_state AS
select  
    `year`, state, family,
    COALESCE(min(sales),0) as sales_min,
	COALESCE(max(sales),0) as sales_max,
 	COALESCE(avg(sales),0) as sales_avg,
    COALESCE(sum(sales),0) as sales_total
from full_df
group by `year`, state, family, sales;
