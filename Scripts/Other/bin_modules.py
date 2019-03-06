hexstr='5555555595555A65556AA696AA6666666955'
print (len(hexstr))
"""
曼彻斯特编码（Manchester Encoding），也叫做相位编码（ Phase Encode，简写PE），
是一个同步时钟编码技术，被物理层使用来编码一个同步位流的时钟和数据。
它在以太网媒介系统中的应用属于数据通信中的两种位同步方法里的自同步法（另一种是外同步法），
即接收方利用包含有同步信号的特殊编码从信号自身提取同步信号来锁定自己的时钟脉冲频率，达到同步目的。
IEEE 802.4（令牌总线）和低速版的IEEE 802.3（以太网）中规定, 按照这样的说法, 01电平跳变表示1, 10的电平跳变表示0。
"""
calc_result = ""
bin_result = bin(int(hexstr,16))
print (len(bin_result))
bin_result = bin_result[2::]
bin_result = str(bin_result)
cont = len(bin_result) /4
print (bin_result)
#输入必须偶
print (len(bin_result))
print (cont)
while (cont > 0):
	head_result = bin_result[0:4]
	print (head_result + "\n")
	if head_result == "0101":
		calc_result += str("11")
	elif head_result == "0110":
		calc_result += str("10")
	elif head_result == "1010":
		calc_result += str("00")
	elif head_result == "1001":
		calc_result += str("01")
	else:
		Error = ""
	bin_result = bin_result[4::]
	cont = cont - 1
	print (calc_result)
print (calc_result)
input()



