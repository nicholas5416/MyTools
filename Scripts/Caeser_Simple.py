def decode_caser():
   d = 'abcdefghijklmnopqrstuvwxyz'
   s = 'gmbh{4d850d5c3c2756f67b91cbe8f046eebd}'
   result = ''

   for i in s:
       if i in d:
           n = d.index(i)
           i = d[n-1]
       print(i,end='')
   result.join(i)
   return result

print(decode_caser())
decode_caser()