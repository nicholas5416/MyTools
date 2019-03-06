a = 16546484
M = 15424654874903
G = (6478678675, 5636379357093)
K = (0, 0)


def add(A, B):
    if A == (0, 0):
        return B
    if B == (0, 0):
        return A
    x1, y1 = A
    x2, y2 = B
    if A != B:
        p = (y2 - y1) * pow(x2 - x1, M - 2, M)
    else:
        p = (3 * x1 * x1 + a) * pow(2 * y1, M - 2, M)
    x3 = p * p - x1 - x2
    y3 = p * (x1 - x3) - y1
    return (x3 % M, y3 % M)


for i in range(546768):
    K = add(K, G)
print 'XUSTCTF{%d}' % (K[0] + K[1])
# XUSTCTF{19477226185390}



"""
已知椭圆曲线加密Ep(a,b)参数为

p = 15424654874903

a = 16546484

b = 4548674875

G(6478678675,5636379357093)

私钥为

k = 546768

求公钥K(x,y)

提示：K=kG

提交格式XUSTCTF{x+y}(注意，大括号里面是x和y加起来求和，不是用加号连接)

注：题目来源XUSTCTF2016

那就先来了解一下ECC

ECC全称为椭圆曲线加密，EllipseCurve Cryptography，是一种基于椭圆曲线数学的公钥密码。与传统的基于大质数因子分解困难性的加密方法不同，ECC依赖于解决椭圆曲线离散对数问题的困难性。它的优势主要在于相对于其它方法，它可以在使用较短秘钥长度的同时保持相同的密码强度。目前椭圆曲线主要采用的有限域有

以素数为模的整数域GF(p)，通常在通用处理器上更为有效。
特征为2的伽罗华域GF（2^m），可以设计专门的硬件。
"""
