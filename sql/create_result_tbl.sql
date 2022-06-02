-- select MAX(season) from GAMES_WIN_LOSS;

-- SELECT * FROM GAMES_WIN_LOSS LIMIT 10;


CREATE TABLE GB_RESULT_2021 as
select * , 
	         CASE
				when gwl.home_team = 'GB' then home_result 
				else away_score - home_score end as GB_RESULT
from GAMES_WIN_LOSS GWL
WHERE GWL.season = 2021
and (GWL.away_team = 'GB' OR GWL.home_team = 'GB');