USE time_series;

CREATE OR REPLACE VIEW full_df AS
    SELECT 
        tr.id,
        tr.family,
        tr.sales,
        tr.onpromotion,
        city,
        state,
        cluster,
        locale,
        locale_name,
        description,
        transferred,
        st.`type`,
        hols.`type` hol_type,
        tr.store_nbr,
        tr.`date`,
        YEAR(tr.`date`) `year`,
        MONTH(tr.`date`) `month`,
        DAY(tr.`date`) `day_of_month`,
        transactions,
        o.dcoilwtico
    FROM
        train AS tr
            LEFT JOIN
        stores AS st ON tr.store_nbr = st.store_nbr
            LEFT JOIN
        holidays_events hols ON tr.`date` = hols.`date`
            LEFT JOIN
        transactions txn ON tr.`date` = txn.`date`
            AND tr.store_nbr = txn.store_nbr
            LEFT JOIN
        oil o ON tr.`date` = o.`date`