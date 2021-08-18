import re
import math
import requests
from flask import Flask, render_template ,request

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/user/<userId>/', methods=['GET'])

def user(userId):
    s = requests.session()
    getInfo = s.get('https://src.sjtu.edu.cn/profile/'+userId)
    if(getInfo.status_code == 200):
        getData = getInfo.text
        userName = re.findall('<h3 class="am-panel-title am-fl">(\S+)',getData)[0]
        userVul = re.findall('总提交漏洞数量： (\d+)',getData)[0]
        userPass = re.findall('已审核通过漏洞数量： (\d+)',getData)[0]
        userRank = re.findall('Rank： (\d+)',getData)[0]
        userLevel = re.findall('等级： <span class="am-badge am-badge-(.*)">(\S+)</span>',getData)[0][1]
        userWin = round((int(userPass)/int(userVul))*100,2)
        listPage = math.ceil(int(userPass)/10)

        list1,list2,badgeList = [],[],[]
        for i in range(1,listPage+1):
            xxx = s.get('https://src.sjtu.edu.cn/profile/'+userId+'/?page='+str(i)).text
            vul_info = re.findall('(\S+)存在(.*)',xxx)
            badgeInfo = re.findall('">(\S+)</span></td>',xxx)
            list1.append(vul_info)
            badgeList.append(badgeInfo)
        for i in range(listPage):
            for j in range(len(list1[i])):
                list2.append(list1[i][j])

        eduDict,vulDict,badgeDict = {},{},{}
        for i in range(len(list2)):
            eduDict[list2[i][0]] = eduDict.get(list2[i][0], 0) + 1
            eduTop = sorted(eduDict.items(),key=(lambda x:x[1]), reverse=True)
        for i in range(len(list2)):
            vulDict[list2[i][1]] = vulDict.get(list2[i][1], 0) + 1
            vulTop = sorted(vulDict.items(),key=(lambda x:x[1]), reverse=True)
        for i in range(len(badgeList)):
            for key in badgeList[i]:
                badgeDict[key] = badgeDict.get(key, 0) + 1
            badgeTop = sorted(badgeDict.items(),key=(lambda x:x[1]), reverse=True)
    else:
        return '404'

    return render_template('user.html',
        userName = userName,
        userVul = userVul,
        userPass = userPass,
        userLevel = userLevel,
        userRank = userRank,
        userWin = userWin,
        eduTop = eduTop,
        vulTop = vulTop,
        badgeTop = badgeTop
    )

if __name__ == '__main__':
    app.run()

