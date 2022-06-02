--CREATE LIST OF DATES TO INFORM SCRAPING
--GROUPED BY GAME WEEK
create table GB_DATES_INTERIM AS
SELECT GB.gameday as gameday,
				 strftime('%W', gb.gameday) week_num,
				 strftime('%Y', gb.gameday) year
FROM GB_RESULT_2021 GB
inner join calendar c
on gb.gameday = c.d;

CREATE TABLE GB_DATES_2021 AS
SELECT GB.*,
				 C.D DATE_ALL,
				 C.weekday,
				 C.MONTH,
				 C.day
FROM GB_DATES_INTERIM GB
INNER JOIN CALENDAR C
ON  (GB.YEAR= C.YEAR AND GB.WEEK_NUM=C.WEEK_NUMBER);

DROP TABLE GB_DATES_INTERIM;