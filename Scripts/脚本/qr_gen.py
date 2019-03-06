#!/usr/bin/env python
import Image
MAX = 27
pic = Image.new("RGB",(MAX, MAX))
str = "000000000000000000000000000011111110100001001011111110010000010110011001010000010010111010001001101010111010010111010010010110010111010010111010111100000010111010010000010100010010010000010011111110101010101011111110000000000000001101000000000011110110010001111101100110000111100001101001010011110000011111101001000110100000001000001000010110000101100001111010100101101001011010011000001110010111100101110011100010010110100101101000001000001111111111000001010010010110111111101111100000000000000010001001000110100011111110000110001010111000010000010100010101000111100010111010011001101111100010010111010100001001000011010010111010101110011101100110010000010100110011001011110011111110100000011100110010000000000000000000000000000"
i=0
for y in range (0,MAX):
    for x in range (0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0, 0, 0))
        else:
            pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("flag.png")