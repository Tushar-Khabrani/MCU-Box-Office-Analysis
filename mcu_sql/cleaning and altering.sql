set sql_safe_updates = 0;
select count(*) from mcu_raw;
alter table mcu_raw drop column ref_col;
delete from mcu_raw where film = 'Total';
update mcu_raw 
set budget = replace(budget, char(0xe2,0x80,0x93), '-');
select * from mcu_raw ;
drop table if exists mcu_clean;
create table mcu_clean (
sr_no int,
film varchar(100),
release_date date,
us_canada_bo bigint,
other_territories_bo bigint,
worldwide_bo bigint,
us_rank int,
ww_rank int,
budget_min bigint,
budget_max bigint,
budget_avg bigint,
phase varchar(20),
release_year int,
release_month int,
roi decimal(10,2),
profit bigint );

insert into mcu_clean
select
cast(sr_no as unsigned),
film,
str_to_date(release_date, '%M %d, %Y'),
cast(replace(replace(us_canada_bo, '$', ''), ',', '') as unsigned),
cast(replace(replace(other_territories_bo, '$', ''), ',', '') as unsigned),
cast(replace(replace(replace(worldwide_bo, '$', ''), ',', ''), '[e]', '') as unsigned),
cast(us_rank as unsigned),
cast(ww_rank as unsigned),
cast(trim(substring_index(replace(replace(budget,'$',''),' million',''),'-',1)) as decimal(10,2)) as budget_min,
cast(trim(substring_index(replace(replace(budget,'$',''),' million',''),'-',-1)) as decimal(10,2)) as budget_max,
(cast(trim(substring_index(replace(replace(budget,'$',''),' million',''),'-',1)) as decimal(10,2)) +
cast(trim(substring_index(replace(replace(budget,'$',''),' million',''),'-',-1)) as decimal(10,2))) / 2 as budget_avg,
phase,
year(str_to_date(release_date, '%M %d, %Y')),
month(str_to_date(release_date, '%M %d, %Y')),
0,
0
from mcu_raw where sr_no != '';

update mcu_clean
set
budget_min = budget_min * 1000000,
budget_max = budget_max * 1000000,
budget_avg = budget_avg * 1000000;

update mcu_clean
set
roi = round((worldwide_bo - budget_avg) / budget_avg, 2),
profit = worldwide_bo - budget_avg;

select * from mcu_clean;
  