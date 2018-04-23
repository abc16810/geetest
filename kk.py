# coding: utf-8
from PIL import Image


def is_pixel_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    if (abs(pix1[0] - pix2[0] < 60) and abs(pix1[1] - pix2[1] < 60) and abs(pix1[2] - pix2[2] < 60)):
        return True
    else:
        return False


img1 = Image.open("7cd7985283644bf0a4af60466df388bf.png")
img2 = Image.open("e33da04454fd489baa48e5ce9d8082a4.png")


w1, h1 = img1.size
w2, h2 = img2.size
if w1 != w2 or h1 != h2:
    print("图片大小不一样")
        
left = 0
flag = False
y = 0
# 划框的宽度大约为60 或者61
# 计算出到凹凸的部位的x轴的宽度即 x_offset
for i in range(61, w1):
    for j in range(h1-25):
        if not is_pixel_equal(img1, img2, i, j):
            left = i
            print(i,j)
            flag = True
            break
    if flag:
        break


if left == 61:
    left -= 2
else:
    left = left - 61

print(left)
