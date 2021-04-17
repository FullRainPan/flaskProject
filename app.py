import pymysql
from flask import Flask, render_template

app = Flask(__name__)


def query(sql):
    conn = pymysql.connect(host='129.211.85.31', user='root', password='Pfclr13366616376asd', database='fr_work')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return list(result)


@app.route('/')
def home():
    sql1 = """
        SELECT COALESCE(服务员工,'总计'),
            COUNT(客户名称),
            SUM(纳税人类型 = '一般纳税人'),
            SUM(纳税人类型 = '小规模纳税人'),
            AVG(月服务费),
            SUM(月服务费) 
        FROM customer 
            WHERE 客户状态 = '正常' 
        GROUP BY 服务员工
        WITH ROLLUP
            """
    sql = """
        SELECT
            customer.客户编号,
            customer.客户简称,
            customer.统一社会信用代码,
            customer.月服务费,
            finance.end_month AS 最后收费账期,
            finance.account AS 缴款方式,
            finance.money AS 本次实收,
            finance.account_date AS 收费日期,
            finance.drawee AS 缴费人,
            customer.开始服务日期 AS 服务日期
        FROM
            customer,
            finance 
        WHERE
            客户状态 NOT IN ( '注销', '转走', '失联' ) 
            AND customer.客户简称 = finance.customer 
            AND finance.detailed_subjects = '会计服务' 
            AND finance.second_subjects = '主营业务收入'
        GROUP BY
            customer.客户简称
        ORDER BY
            customer.客户编号
                """
    result = query(sql1)
    items = query(sql)
    return render_template('upload.html', result=result, items=items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
