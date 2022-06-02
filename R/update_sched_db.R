library(nflfastR)
library(DBI)
library(RSQLite)

con <- dbConnect(RSQLite::SQLite(), "~/Projects/Acipenser/database/nfl.db")

df = fast_scraper_schedules(1999:2021)

dbWriteTable(con, 'GAMES_WIN_LOSS', df, overwrite=TRUE)
dbDisconnect(con)
