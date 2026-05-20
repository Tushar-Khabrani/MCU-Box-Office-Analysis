select film, worldwide_bo from mcu_clean 
order by worldwide_bo desc limit 1;
select film, worldwide_bo from mcu_clean 
order by worldwide_bo desc limit 10;
select film, worldwide_bo from mcu_clean 
order by worldwide_bo asc limit 1;
select phase, 
sum(worldwide_bo) as total_earning,
count(film) as total_films
from mcu_clean 
group by phase order by phase;
select phase,
round(avg(worldwide_bo), 2) as avg_earning,
round(avg(budget_avg), 2) as avg_budget
from mcu_clean
group by phase order by phase;
select release_year,
sum(worldwide_bo) as total_earning,
count(film) as films_released
from mcu_clean
group by release_year order by release_year;
select film, budget_avg, worldwide_bo, roi, profit
from mcu_clean where roi >= 2 order by roi desc;
select film, budget_avg, worldwide_bo, roi, profit
from mcu_clean where roi < 1 order by roi asc;

