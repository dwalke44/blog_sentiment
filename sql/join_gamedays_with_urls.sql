--GROUP URLS BY GAME WEEK
drop table GB_DATES_URLS_21;
CREATE TABLE GB_DATES_URLS_21 AS
SELECT GB_DATES_2021.CALDATE,
			 GB_DATES_2021.GAMEDATE, 
			 GB_URLS.loc URL,
			 strftime('%Y-%m-%d', GB_URLS.lastmod) PUB_DATE
from GB_URLS
inner JOIN GB_DATES_2021
ON  strftime('%Y-%m-%d', GB_DATES_2021.CALDATE) = strftime('%Y-%m-%d', GB_URLS.lastmod)
order by 1;

select distinct gamedate from GB_DATES_URLS_21;
