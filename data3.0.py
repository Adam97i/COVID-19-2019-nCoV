import requests, os
import xlwt
import time
import json


class COVID_19:
    def __init__(self, times, sleeptime):
        self.times = times
        self.sleeptime = sleeptime
        self.col = 0
        self.starttime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.file_path = 'E:/疫情人数4.0/'

        self.save_data_to_excle()

    def get_data(self):
        data = {}
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
        # print(json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children'])
        for item in json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children']:
            if item['name'] not in data:
                data.update({item['name']: 0})
            newadd = all = heal = dead = 0
            i = 0
            pcity = dict()
            for city_data in item['children']:
                # data[item['name']] += int(city_data['total']['confirm'])
                # print(city_data)

                cname = city_data['name']
                cadd = int(city_data['today']['confirm'])
                call = int(city_data['total']['confirm'])
                cheal = int(city_data['total']['heal'])
                cdead = int(city_data['total']['dead'])

                city = {'cname': cname, 'cadd': cadd, 'call': call, 'cheal': cheal, 'cdead': cdead}

                newadd += cadd
                all += call
                heal += cheal
                dead += cdead
                pcity[i] = city
                i += 1
                # pcity = pcity.copy()
                # pcity.update(city)
                data[item['name']] = (newadd, all, heal, dead, pcity)

        return data

    def get_foreign_data(self):
        data_f = {}
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&callback%d' % int(time.time() * 1000)
        # print(json.loads(requests.get(url=url).json()['data'])['foreignList'])
        data_f = json.loads(requests.get(url=url).json()['data'])['foreignList']
        return data_f

    def save_data_to_excle(self):
        self.make_dir()
        # 调用方法检查数据目录是否存在，不存在则创建数据文件夹

        # 数据写入行数记录
        newworkbook = xlwt.Workbook()

        worksheet = newworkbook.add_sheet('国内')
        worksheet2 = newworkbook.add_sheet('国外')
        # 设置单元格背景色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 5  # 5 背景颜色为黄色
        style = xlwt.XFStyle()
        style.pattern = pattern
        # 打开工作簿，创建工作表
        timecount = 0
        while timecount < self.times:

            if timecount!=0:

                print("Gona sleep for %d seconds" % (self.sleeptime))
                time.sleep(self.sleeptime)
            worksheet.write_merge(0, 0, self.col + 0, self.col + 1,
                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            worksheet.write_merge(0, 0, self.col + 2, self.col + 3, '数据来源：腾讯')
            worksheet.write_merge(0, 0, self.col + 4, self.col + 5, '记录人：adam')

            worksheet2.write_merge(0, 0, self.col + 0, self.col + 1,
                                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            worksheet2.write_merge(0, 0, self.col + 2, self.col + 3, '数据来源：腾讯')
            worksheet2.write_merge(0, 0, self.col + 4, self.col + 5, '记录人：adam')

            worksheet.write(1, self.col + 0, '省')
            worksheet.write(1, self.col + 1, '市')
            worksheet.write(1, self.col + 2, '昨日新增')
            worksheet.write(1, self.col + 3, '累计确诊')
            worksheet.write(1, self.col + 4, '治愈')
            worksheet.write(1, self.col + 5, '死亡')

            worksheet2.write(1, self.col + 0, '国家')
            worksheet2.write(1, self.col + 2, '昨日新增')
            worksheet2.write(1, self.col + 3, '累计确诊')
            worksheet2.write(1, self.col + 4, '治愈')
            worksheet2.write(1, self.col + 5, '死亡')

            # print(self.col)

            # 写入数据列标签
            data = self.get_data()
            # print(data)
            count = 2
            for p in data:
                name = p
                newadd = data[p][0]
                all = data[p][1]
                heal = data[p][2]
                dead = data[p][3]
                # print(name)
                # 用循环获取省级以及该省以下城市的数据
                # print(self.col)
                worksheet.write(count, self.col + 0, name, style)
                worksheet.write(count, self.col + 1, '', style)
                worksheet.write(count, self.col + 2, newadd, style)
                worksheet.write(count, self.col + 3, all, style)
                worksheet.write(count, self.col + 4, heal, style)
                worksheet.write(count, self.col + 5, dead, style)
                count += 1

                for c in data[p][4]:
                    worksheet.write(count, self.col + 1, data[p][4][c]['cname'])
                    worksheet.write(count, self.col + 2, data[p][4][c]['cadd'])
                    worksheet.write(count, self.col + 3, data[p][4][c]['call'])
                    # worksheet.write(counself.col+t, 5, p_suspectedcount)
                    worksheet.write(count, self.col + 4, data[p][4][c]['cheal'])
                    worksheet.write(count, self.col + 5, data[p][4][c]['cdead'])
                    count += 1

            # 国外数据
            # count+=2

            data_f = self.get_foreign_data()
            count = 2
            for c in data_f:
                worksheet2.write(count, self.col + 0, c['name'])
                worksheet2.write(count, self.col + 2, c['confirmAdd'])
                worksheet2.write(count, self.col + 3, c['confirm'])
                worksheet2.write(count, self.col + 4, c['heal'])
                worksheet2.write(count, self.col + 5, c['dead'])
                count += 1

            self.col += 7

            timecount += 1
            print("wrote data count = %d" % timecount)



        end_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        newworkbook.save('%s%s---%s.xls' % (self.file_path,self.starttime,end_time))
        print('======数据爬取成功======')

    def make_dir(self):

        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
            print('======数据文件夹不存在=======')
            print('======数据文件夹创建成功======')
            print('======创建目录为%s======' % (self.file_path))
        else:
            print('======数据保存在目录：%s======' % (self.file_path))
        # 检查并创建数据目录

# COVID_19(2, 3).save_data_to_excle()
if __name__ == '__main__':
    times=2
    sleeptime =3
    # 次数 和睡眠时间 以秒为单位
    COVID_19(times,sleeptime)
