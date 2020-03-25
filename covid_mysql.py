import time, json, requests, pymysql,urllib.request

# 创建数据库
"""
create database covidd;
use covidd;
CREATE TABLE data(
`country` varchar(40),
`time` varchar(20),
`newadd` int ,
`all` int  ,
`heal` int ,
`dead` int ,
`deadRate` varchar(20) ,
`nowConfirm` int(11) default -1 ,
PRIMARY KEY (`country`,`time`)) DEFAULT CHARSET=utf8;
  """

class database(object):
    def __init__(self):
        self.data = list()
        self.conn = pymysql.connect(host='122.51.78.217', port=3306, user='root', password='adam1997..', db='covid',
                                    charset='utf8')
        self.now = time.strftime("%m.%d", time.localtime())
        print('conected mysql successfully')

    def get_china_data(self):

        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
        # china = json.loads(requests.get(url=url).json()['data'])['areaTree'][0]
        china = json.loads(requests.get(url=url).json()['data'])['chinaTotal']
        add = json.loads(requests.get(url=url).json()['data'])['chinaAdd']['confirm']
        # print(china)
        # for item in json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children']:

        # 国家 时间 新增 总计 治愈 死亡 死亡率 现存确诊
        infos = ('中国', self.now, add, china['confirm'], china['heal'],
                 china['dead'], round(100 * china['dead'] / china['confirm'], 2), china['nowConfirm'])
        self.data.append(infos)
        return

    def get_foreign_data(self):
        # data_f = {}

        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
        resp = urllib.request.urlopen(url)
        data = json.loads(resp.read())['data']
        data_f= json.loads(data)['foreignList']
        for d in data_f:
            infos = (d['name'], d['date'], d['confirmAdd'], d['confirm'], d['heal'], d['dead'],
                     round(100 * d['dead'] / d['confirm'], 2), d['nowConfirm'])
            # print(infos)
            self.data.append(infos)
        return

    def insert_data(self):
        cursor = self.conn.cursor()
        try:
            delete_sql = "delete from data where  time ='%s' " % (self.now)
            cursor.execute(delete_sql)
        finally:

            self.get_china_data()
            self.get_foreign_data()

            for d in self.data:
                # print(d[0], d[1], d[2], d[3], d[4], d[5], d[6])
                # print(type(d[0]),type(d[1]),type(d[2]),type(d[3]),type(d[4]),type(d[5]),type(d[6]))
                if d[1] == self.now:
                    # sql="INSERT INTO data (country,time,newadd,all,heal,dead,deadRate) VALUES ('%s','%s','%d','%d','%d','%d','%s');" % (d[0], d[1], d[2], d[3], d[4], d[5], d[6])
                    sql = "INSERT INTO data VALUES ('%s','%s','%d','%d','%d','%d','%s','%d');" % (
                        d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
                    print(sql)
                    cursor.execute(sql)
            print('insert successfully')
            # 关闭连接，游标和连接都要关闭
            self.conn.commit()
            self.data=list()
            cursor.close()

    def select_data(self):
        cursor = self.conn.cursor()
        get_data_sql = "select *  from data where  time ='%s' " % (self.now)
        cursor.execute(get_data_sql)
        daily = cursor.fetchall()
        cursor.close()
        attribute = ['name', 'date', 'newadd', 'all', 'heal', 'dead', 'deadRate', 'nowconfirm']
        daily_data = list()
        for i in daily:
            i = list(i)
            daily_data.append(dict(zip(attribute, i)))

        data = json.dumps(daily_data, indent=2, ensure_ascii=False)

        return data

    def close_connection(self):
        self.conn.close()

a= database()
a.insert_data()
