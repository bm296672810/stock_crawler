import json
import sqlite3 as sql
import re
# 解析request里get_stock_list请求的数据
def parse_stock_list(json_str):
    fo = open('stack_list.txt', 'w')
    fo.write(json_str)
    fo.close()
    json_dict = json.loads(json_str)

    conn = sql.connect('stock.db')
    c = conn.cursor()
    c.execute("begin")

    curr_pageno = 1
    page_count = 0
    for d in json_dict:
        data       = d["data"]
        if len(data) == 0:
            continue

        mate_data   = d["metadata"]
        pagesize    = mate_data["pagesize"]     # 当前页的数量
        pageno      = mate_data["pageno"]        # 当前页号
        pagecount   = mate_data["pagecount"]     # 总页数
        conditions  = mate_data["conditions"]    # 条件查询的数据 其中第二项是行业
        curr_pageno = pageno
        page_count  = pagecount

        for i in conditions:
            if i["label"] == "行业类别":
                ops   = i["options"]
                for o in ops:
                    text  = o["text"]
                    value = o["value"]
                    if value != "":
                        
                        trade_sql = '''insert into t_trade (id, value, name) values(NULL, '%s', '%s')''' % (value, text[2:])
                        # result = c.execute(trade_sql)
                        try:
                            c.execute(trade_sql)
                        except sql.IntegrityError as e:
                            print("execute:%s error: %s" % (trade_sql, e))
                
            if i["label"] == "板块":
                ops   = i["options"]
                for o in ops:
                    text  = o["text"]
                    value = o["value"]
                    if value != "":
                        plate_sql = '''insert into t_plate (id, value, name) values(NULL, '%s', '%s')''' % (value, text)
                        try:
                            c.execute(plate_sql)
                        except sql.IntegrityError as e:
                            print("excute:%s error: %s" % (plate_sql, e))
                
        for m in data:
            bk     = m["bk"]        # 板块
            agdm   = m["agdm"]      # A股代码
            agjc   = m["agjc"]      # A股简称
            agssrq = m["agssrq"]    # 上市日期
            agzgb  = m["agzgb"]     # 总股本
            agltgb = m["agltgb"]    # 流通股本
            sshymc = m["sshymc"]    # 所属行业

            if bk == "中小板":
                bk = "中小企业板"

            jc = re.sub('\'', '\'\'', agjc)
            stock_sql = '''insert into t_stock (id, code, little_name, launch_date, stock_count, 
            circulte_count, plate_id, trade_id) values(NULL, '%s', '%s', '%s', '%s', '%s', 
            (SELECT id FROM t_plate WHERE name = '%s'), (SELECT id FROM t_trade WHERE value = '%s'))
            ''' % (agdm, jc, agssrq, agzgb, agltgb, bk, sshymc[0:1])
            try:
                c.execute(stock_sql)
            except :
                print("execute: %s occure Error" % stock_sql)
    try:    
        c.execute("commit")
    except sql.OperationalError as e:
        print("commit error: %s" % e)

    c.close()

    return (curr_pageno, page_count)

# 解析request里 get_time_data请求的数据
def parse_data_json(json_str):
    json_dict = json.loads(json_str)
    try:
        # date_time = json_dict["datetime"]
        code          = json_dict["code"]
        j_data        = json_dict["data"]
        code          = j_data["code"]          # 股票代码
        name          = j_data["name"]          # 股票名字
        close         = j_data["close"]         # 昨收价
        open          = j_data["open"]          # 开盘价
        now           = j_data["now"]           # 最新价
        high          = j_data["high"]          # 最高点
        low           = j_data["low"]           # 最低点
        volume        = j_data["volume"]        # 成交量(手)
        amount        = j_data["amount"]        # 成就额(元)
        delta         = j_data["delta"]         # 涨跌价
        delta_precent = j_data["deltaPercent"]  # 涨跌幅(%)
        market_time   = j_data["marketTime"]    # 时间
        picupdata     = j_data["picupdata"]     # 分钟数据
        print("time | curr_price | avarge_price | delta | delta_precent | volume | amount")
        conn = sql.connect('stock.db')
        c = conn.cursor()
        sql_ov = '''insert into t_stock_overview (id, stock_id, close, open, 
        now, high, low, volume, amount, delta, delta_precent, market_time) 
        values (NULL, (select id from t_stock where code='%s'), '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        ''' % (code, close, open, now, high, low, volume, amount, delta, delta_precent, market_time)

        c.execute("begin")
        try:
            c.execute(sql_ov)

            course = c.execute("select max(id) as id from t_stock_overview")
            stock_ov_id = course.lastrowid

            try:
                for data in picupdata:
                    t = data[0]     # 时间
                    cp = data[1]    # 最新价
                    ap = data[2]    # 平均价
                    d = data[3]     # 涨跌
                    dp = data[4]    # 涨跌幅(%)
                    v = data[5]     # 成交量(手)
                    a = data[6]     # 成交额(元)
                    # print("%s | %s | %s | %s | %s | %s | %s" % (t, cp, ap, d, dp, v, a))
                    sql_mi = '''insert into t_stock_mintly (id, stock_overview_id, time, now,
                    avarge_price, delta, delta_precent, volume, amount) values (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                    ''' % (stock_ov_id, t, cp, ap, d, dp, v, a)

                    try:
                        c.execute(sql_mi)
                    except :
                        print("execute:%s error" % sql_mi)
            except:
                print("for data error")
                
        except:
            print("execute: %s error" % sql_ov)

        try:    
            c.execute("commit")
        except sql.OperationalError as e:
            print("commit error: %s" % e)

    except ValueError:
        print("except")

# 从数据库查询所有的股票代码
def get_all_code():
    conn = sql.connect('stock.db')
    c = conn.cursor()
    result = []
    r = c.execute("SELECT code FROM t_stock")
    for i in r:
        result.append(i[0])
    c.close()

    return result
