import json,urllib.request,urllib.parse

heads = {}
heads[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'

def get_dianfei():

    getlou = '10#306'

    getlou = getlou.split('#')
    bui = getlou[0].zfill(2)
    if len(getlou[1]) > 4:
        lou = getlou[1][:1]
        lou = urllib.parse.quote(lou)
    else:
        lou = ''
    num = getlou[1][-3:]

    #lou = urllib.parse.quote(lou)

    url = 'http://www.youthol.cn/wechat/elec/index.php?Whe=west&Bui='+bui+'%23'+ lou +'&Num='+num
    #url = urllib.parse.quote(url).encode('utf-8')

    response = urllib.request.Request(url,None,heads)
    response = urllib.request.urlopen(response)
    html = response.read().decode('utf-8')

    jsons = json.loads(html)

    #print(jsons)
    return jsons
    #print(jsons[0][0])

if __name__ == '__main__':
    try:
        jsons = get_dianfei()
        print(jsons[0][0])

        #写入每天读取的数值
        with open("dianfei.txt",'r+') as f:

            c = f.readlines()
            if len(c) > 0:
                c = c[-1]
            f.seek(0,2)
            f.write(jsons[2][0] + "  " + jsons[1][0] + "  " + jsons[3][0] + "  " + jsons[4][0])

            if len(c) != 0:
                sun = c.split('  ')[-3]
                sunhao = float(sun) - float(jsons[3][0])
                f.write("  %.2f"%(sunhao))
            else:
                f.write("  " +'0')
            f.write('\r\n')

        '''
        #读取昨天采集到的用电量
        with open("dianfei.txt",'r+') as f:
            sun = f.readlines()[-2].split('  ')[-2]
            sunhao =float(sun) - float(jsons[3][0])

        #计算所得的耗电量
        with open("haodian.txt",'a+') as f:
            f.write(jsons[2][0])

            if sunhao >= 0:     #判断耗电还是充电
                f.write("    日用电为：%f\r\n"%(sunhao))
            else:
                f.write("    冲入的电量为：%f\r\n"%(0-sunhao))
            print(str(sunhao))
        '''

    except json.decoder.JSONDecodeError:
        print("请输入正确的楼号与房间号！")
    #except IndexError:
        print("请输入正确的楼号与房间号！")
    except KeyboardInterrupt:
        print('退出查询系统！')
    except FileNotFoundError:
        with open("dianfei.txt", 'w+') as f:
            f.write("")
