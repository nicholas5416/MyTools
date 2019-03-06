s="jeihjiiklwjnk{ljj{kflghhj{ilk{k{kij{ihlgkfkhkwhhjgly"

flag=""

for i in s:

    if ord(i)>100 & ord(i)<150:

        flag+=chr(ord(i)-53)

    elif ord(i)<=48:

        flag+=chr(ord(i)/12*11)

    else:

        flag+=chr(ord(i)/60*61)

    print (flag)
