# -*- coding:utf-8 -*-
print ('##=====================================================##')
print ('     URP教务系统自动评课程序    ')
print ('      Powered By Kylinking.     ')
print ('##=====================================================##')
import urllib.request
import urllib.parse
import http.cookiejar
import time
import re
import random

##登录##
def login(user, password, code):
    flag = 0
    url = 'http://xxx.edu.cn/loginAction.do'         ##登录地址
    data = {}
    data['dzslh'] = ''
    data['eflag'] = ''
    data['evalue'] = ''
    data['fs'] = ''
    data['lx'] = ''
    data['tips'] = ''
    data['zjh1'] = ''
    data['zjh'] = user
    data['mm'] = password
    data['v_yzm'] = code
    header = {}
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Accept-Encoding'] = 'gzip, deflate'
    header['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    header['Connection'] = 'keep-alive'
    header['Host'] = 'xxx.edu.cn'
    header['Referer'] = 'http://xxx.edu.cn/loginAction.do'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    data = urllib.parse.urlencode(data).encode('gb2312')
    req = urllib.request.Request(url,data,header)
    response = urllib.request.urlopen(req)
    html = response.read().decode('gb2312')
    i = html.find('URP综合教务系统 - 登录')
    if i > 0:
        flag = 0
        print ("尝试登录失败,请重新登录.")
    else:
        flag = 1
        print('登录成功,开始获取选课信息.'+'\n')
    return flag

##获取cookie##
def setCookie():
    cookie = http.cookiejar.CookieJar() 
    cookieProc = urllib.request.HTTPCookieProcessor(cookie) 
    opener = urllib.request.build_opener(cookieProc) 
    urllib.request.install_opener(opener)

##提取验证码(手动输入验证码)##
def getVerify():
    setCookie()
    vrifycodeUrl = 'http://xxx.edu.cn/validateCodeAction.do'
    file = urllib.request.urlopen(vrifycodeUrl)
    pic= file.read()
    path = 'd:\\code.jpg'
    try:
        localpic = open(path, 'wb')
        localpic.write(pic)
        localpic.close()
        print ('获取验证码成功,%s.' %path)
    except IOError:
        print ('获取验证码失败,请重新运行程序.')
    code = input("验证码: ")
    return code

courseList = {}
bpr = {}            ##课序号
pgnr = {}           ##课程号
bprm = {}           ##教师
pgnrm = {}          ##课程名
isActive = {}

##获取选课信息##
def getInfo():
    header = {} 
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Accept-Encoding'] = 'gzip, deflate'
    header['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    header['Connection'] = 'keep-alive'
    header['Host'] = 'xxx.edu.cn'
    header['Referer'] = 'http://xxx.edu.cn/jxpgXsAction.do?oper=listWj'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    url = 'http://xxx.edu.cn/jxpgXsAction.do?oper=listWj'        ##获取选课信息地址
    response = urllib.request.urlopen(url)
    html = response.read().decode('gb2312')
    sub = "<img name="
    count = html.count(sub, 0, len(html))
    print("课程数目:", count)
    for i in range(0, count):
        m = html.find(sub)
        m = m + 10
        html = html[m:]
        n = html.find('style="cursor: hand;')
        bqr1 = html[:n]
        courseList[i] = bqr1
    for i in range(0, count):
        tmp = courseList[i]
        m = tmp.find('#@')
        n = tmp.find('"')
        o = tmp.find('2015-2016-1-xs')
        bpr1 = tmp[m+2:m+8]
        if (tmp[n-11:n-10] != '@'):         ##处理选修课,选修课的课序号多一位
            pgnr1 = tmp[n-11:n-2]
            pgnrm1 = tmp[o+16:n-13]
        else:
            pgnr1 = tmp[n-10:n-2]
            pgnrm1 = tmp[o+16:n-12]
        bprm1 = tmp[m+10:o-2]
        bpr[i] = bpr1
        pgnr[i] = pgnr1
        bprm[i] = bprm1
        pgnrm[i] = pgnrm1
    for i in range(0, count):
        isActive[i] = 1
        print ('课程号:'+bpr[i])
        print ('课序号:'+pgnr[i])
        print (pgnrm[i]+' '+bprm[i]+'\n')
        o = html.find('src="/img/icon/view.gif"')
        if (o > 0):
            isActive[i] = 0
    return count

##提交评课信息##
def postPj(br, pr, bm, pm):
    preheader = {}
    preheader['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    preheader['Accept-Encoding'] = 'gzip, deflate'
    preheader['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    preheader['Connection'] = 'keep-alive'
    preheader['Host'] = 'xxx.edu.cn'
    preheader['Referer'] = 'http://xxx.edu.cn/jxpgXsAction.do?oper=listWj'
    preheader['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    predata = {}
    predata['wjbm'] = '0000000006'
    predata['bpr'] = br         ##课序号
    predata['pgnr'] = pr        ##课程号
    predata['oper'] = 'wjShow'
    predata['wjmc'] = '2015-2016-1-xs'
    predata['bprm'] = bm        ##教师
    predata['pgnrm'] = pm       ##课程名
    predata['wjbz'] = 'null'
    predata['pageSize'] = '20'
    predata['page'] = '1'
    predata['currentPage'] = '1'
    predata['pageNo'] = ''
    preurl = 'http://xxx.edu.cn/jxpgXsAction.do'
    predata['bprm'] = predata['bprm'].encode('gbk')         ##教师名和课程名是以gbk编码的，更改后提交无法获得正确响应
    predata['pgnrm'] = predata['pgnrm'].encode('gbk')
    predata = urllib.parse.urlencode(predata).encode(encoding='gb2312')
    prereq = urllib.request.Request(preurl,predata,preheader)
    preresponse = urllib.request.urlopen(prereq)
    prehtml = preresponse.read().decode('gb2312')
    
    pjheader = {}
    pjheader['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    pjheader['Accept-Encoding'] = 'gzip, deflate'
    pjheader['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    pjheader['Connection'] = 'keep-alive'
    pjheader['Host'] = 'xxx.edu.cn'
    pjheader['Referer'] = 'http://xxx.edu.cn/jxpgXsAction.do'
    pjheader['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    data = {}
    data['wjbm'] = '0000000006'
    data['bpr'] = br
    data['pgnr'] = pr
    data['xumanyzg'] = 'zg'
    data['wjbz'] = ''
    ##评价选项，默认为优秀，5_1表示优秀，5_0.8表示良好，5_0.6表示正常，以此类推
    data['0000000047'] = '5_1'
    data['0000000048'] = '5_1'
    data['0000000049'] = '5_1'
    data['0000000050'] = '5_1'
    data['0000000051'] = '5_1'
    data['0000000052'] = '5_1'
    data['0000000053'] = '5_1'
    data['0000000054'] = '5_1'
    data['0000000055'] = '5_1'
    data['0000000056'] = '5_1'
    data['0000000057'] = '5_1'
    data['0000000058'] = '5_1'
    data['0000000059'] = '5_1'
    data['0000000060'] = '5_1'
    data['0000000061'] = '5_1'
    data['0000000062'] = '5_1'
    data['0000000063'] = '5_1'
    data['0000000064'] = '5_1'
    data['0000000065'] = '5_1'
    data['0000000066'] = '5_1'
    data['zgpj'] = '.'          ##主观评价
    data = urllib.parse.urlencode(data).encode('gb2312')
    pjurl = 'http://xxx.edu.cn/jxpgXsAction.do?oper=wjpg'            ##提交评价结果页面
    pjreq = urllib.request.Request(pjurl,data,pjheader)
    pjresponse = urllib.request.urlopen(pjreq)
    pjhtml = pjresponse.read().decode('gb2312')
    i = pjhtml.find('评估成功')
    if (i > 0):
        print (pm + ' ' + bm+ ' 评价成功!')

if __name__ == '__main__':
    user = input('学号: ')
    password = input('密码: ')
    code = getVerify()
    if (login(user, password, code) == 1):
        count = getInfo()
        for i in range(0, count):
            if (isActive[i] == 0):
                print (pgnrm[i]+' 该课程已评价.')
            else:
                postPj(bpr[i], pgnr[i], bprm[i], pgnrm[i])
        print ('\n'+'课程评价完毕.')

