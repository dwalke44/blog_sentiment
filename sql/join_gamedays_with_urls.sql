--SELECT count(*) FROM GB_URLS;
-- drop table GB_URLS;
-- select DATE_ALL FROM GB_DATES_2021;
-- SELECT * FROM GB_DATES_2021 LIMIT 10;


--GROUP URLS BY GAME WEEK

CREATE TABLE GB_DATES_URLS_21 AS
select GB_URLS.loc BLOG_URL,
			 strftime('%Y-%m-%d', lastmod) PUB_DATE,
			 GB2.gameday GAMEDAY
from GB_URLS
INNER JOIN GB_DATES_2021 GB2
ON  strftime('%Y-%m-%d', GB_URLS.lastmod) = GB2.DATE_ALL
order by 2;