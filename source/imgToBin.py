'''
单张图片二值化结果存为二进制文件的脚本
'''

import cv2

def toBinFile(img): # 转换为二进制文件，扫描方式为数据水平，字节垂直，字节内数据反序（适合我自己的工程）
    height = len(img)
    width = len(img[0])
    with open('../output/output.mmc', 'wb+') as f:
        for i in range(height//8):
            for j in range(width):
                byte = ''
                for k in range(8):
                    byte += str(img[i*8+7-k][j])
                s = bytes([int(byte,2)])
                f.write(s)


if __name__ == '__main__':
    img = cv2.imread('../images/huiye384.jpg', 0)  # 直接读为灰度图像
    img = cv2.resize(img, (128, 64))  # 将图片zoom到指定大小
    ret, th = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    toBinFile(th)