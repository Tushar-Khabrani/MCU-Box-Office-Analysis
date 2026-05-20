load data local infile 'C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu.csv'
into table mcu_raw
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 rows
(@col1, film, release_date, us_canada_bo, other_territories_bo, worldwide_bo, us_rank, ww_rank, budget, ref_col, phase)
set sr_no = @col1;
select * from mcu_raw;