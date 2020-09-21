-- value  行业代号
-- name   行业名称
CREATE TABLE t_trade(
    id INTEGER PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL ON CONFLICT ROLLBACK,
		value CHAR[2] NOT NULL UNIQUE,
		name CHAR[100]
);

-- value 板块代码
-- name  板块名称
CREATE TABLE t_plate(
    id INTEGER PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL ON CONFLICT ROLLBACK,
		value CHAR[2] NOT NULL UNIQUE,
		name CHAR[100]
);
-- code           股票代码
-- little_name    股票简称
-- launch_date    上市日期
-- stock_count    总股本(亿股)
-- circulte_count 流通股本(亿股)
-- trade_id       行业id
CREATE TABLE t_stock(
    id INTEGER PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL ON CONFLICT ROLLBACK,
		code CHAR[10] NOT NULL UNIQUE ON CONFLICT ROLLBACK,
		little_name CHAR[20],
		launch_date CHAR[30],
		stock_count CHAR[50],
		circulte_count CHAR[50],
		plate_id INT,
		trade_id INT
);

CREATE TABLE t_stock_overview(
   id INTEGER PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL ON CONFLICT ROLLBACK,
   stock_id INT,
	 close CHAR,
	 open CHAR,
	 now CHAR,
	 high CHAR,
	 low CHAR,
	 volume CHAR,
	 amount CHAR,
	 delta CHAR,
	 delta_precent CHAR,
	 market_time CHAR,
	 CONSTRAINT ct_stock_day UNIQUE(stock_id, market_time)
);
-- stock_day_id is stock_day index
-- time is the mintly time the formate 9:30/9:31/14:30
-- now is the latest price
-- avarge_price The average over this minute
-- delta delta_precent
CREATE TABLE t_stock_mintly(
   id INTEGER PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL ON CONFLICT ROLLBACK,
	 stock_overview_id INT,
	 `time` CHAR,
	 now CHAR,
	 avarge_price CHAR,
	 delta CHAR,
	 delta_precent CHAR,
	 volume CHAR,
	 amount CHAR,
	 CONSTRAINT ct_stock_mintly UNIQUE(stock_overview_id, `time`)
);