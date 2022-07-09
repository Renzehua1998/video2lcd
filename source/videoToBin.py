'''
视频二值化结果存为二进制文件的脚本
'''
import cv2
import os
import sys

def videoToFrames(camera, freq=1, folder='frameOutput', types='jpg'): # 视频提取帧保存到本地
    times = 0
    fileName = 0

    # 提取视频的频率，每1帧提取一个
    frame_frequency = freq

    frameNum = camera.get(7)  # 总帧数

    path = '../output/' + folder + '/'
    if not os.path.exists(path):
        os.makedirs(path)  # 可以创建文件夹及子目录

    while True:
        times = times + 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        # 按照设置间隔存储视频帧
        if times % frame_frequency == 0:
            cv2.imwrite(path + str(fileName) + '.' + types, image)
            fileName += 1
            progressBar(times / frameNum) # 显示进度条

    print('图片提取结束')
    # 释放摄像头设备
    camera.release()

def binImgReverse(img): # 二值化图像取反
    height = len(img)
    width = len(img[0])

    for i in range(height):
        for j in range(width):
            if img[i][j] == 1:
                img[i][j] = 0
            else:
                img[i][j] = 1
    return img

def progressBar(percent): # 进度条代码
    print("\r", end="")
    print("进度: {:.2f}%: ".format(percent*100), "▓" * (int(percent*100) // 2), end="")
    sys.stdout.flush()

# 视频提取帧转换为bin文件
# 输入视频帧，提取间隔（默认3），转换模式（全局、局部），
# 输出是否反转（默认否），字节是否反序（默认否），
# 扫描方式 0-3 四种方式：0 水平扫描；1 垂直扫描；2 数据水平，字节垂直；3 数据垂直，字节水平
# 输出文件名（默认video）
def videoToBin(camera, freq=3, transMode='Global', reverse=False, reOrder=False,
               UDFlip=False, RLFlip=False, scanMode=0, output='video'):
    times = 0
    # 提取视频的频率，每1帧提取一个
    frame_frequency = freq

    frameNum = camera.get(7) # 总帧数

    with open('../output/'+output+'.bin', 'wb+') as f:
        while True:
            times = times + 1
            res, img = camera.read()
            if not res:
                print('not res , not image')
                break
            # 按照设置间隔存储视频帧
            if times % frame_frequency == 0:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (128, 64))  # 将图片zoom到指定大小

                if transMode == 'Global': # 根据转换模式进行转换
                    _, img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                elif transMode == 'Local':
                    img = cv2.adaptiveThreshold(img, 1, cv2.ADAPTIVE_THRESH_MEAN_C, 1, 3, 2)

                if reverse: # 若设置像素反序，此处执行反序代码
                    img = binImgReverse(img)

                if UDFlip: # 若设置上下反转，则执行此代码
                    img = cv2.flip(img,0)

                if RLFlip: # 若设置左右反转，则执行此代码
                    img = cv2.flip(img,1)

                height = len(img)
                width = len(img[0])
                if scanMode==0: # 水平扫描
                    for i in range(height):
                        for j in range(width // 8):
                            byte = ''
                            for k in range(8):
                                byte += str(img[i][j * 8 + k])
                            if reOrder:  # 字节反序
                                byte = byte[::-1]
                            s = bytes([int(byte, 2)])  # 转换为字节数据
                            f.write(s)  # 写入文件
                elif scanMode==1: # 垂直扫描
                    for j in range(width):
                        for i in range(height // 8):
                            byte = ''
                            for k in range(8):
                                byte += str(img[i * 8 + k][j])
                            if reOrder:  # 字节反序
                                byte = byte[::-1]
                            s = bytes([int(byte, 2)])  # 转换为字节数据
                            f.write(s)  # 写入文件
                elif scanMode==2: # 数据水平，字节垂直
                    for i in range(height // 8):
                        for j in range(width):
                            byte = ''
                            for k in range(8):
                                byte += str(img[i * 8 + k][j])
                            if reOrder: # 字节反序
                                byte = byte[::-1]
                            s = bytes([int(byte, 2)]) # 转换为字节数据
                            f.write(s) # 写入文件
                elif scanMode==3: # 数据垂直，字节水平
                    for j in range(width // 8):
                        for i in range(height):
                            byte = ''
                            for k in range(8):
                                byte += str(img[i][j * 8 + k])
                            if reOrder:  # 字节反序
                                byte = byte[::-1]
                            s = bytes([int(byte, 2)])  # 转换为字节数据
                            f.write(s)  # 写入文件
                progressBar(times / frameNum) # 显示进度条

    print('图片转换结束')
    # 释放摄像头设备
    camera.release()

if __name__ == '__main__':
    # 读取视频帧
    camera = cv2.VideoCapture('../videos/辉夜大小姐2OP.mp4')
    # camera = cv2.VideoCapture('../videos/书记舞.mp4')
    # camera = cv2.VideoCapture('../videos/辉夜大小姐3ED2.mp4')
    # camera = cv2.VideoCapture('../videos/早坂爱lulululu.mp4')

    # videoToFrames(camera, freq=3, folder='shuji', types='jpg') # 导出帧图片

    videoToBin(camera, transMode='Local', reOrder=True, scanMode=2, output='测试')
    # videoToBin(camera, transMode='Local', reOrder=True, scanMode=2, output='早坂爱局部') # 导出bin文件
    # videoToBin(camera, transMode='Global', reOrder=True, scanMode=2, output='早坂爱全局')

    # for i in range(19): # 获取视频的详细参数 见/source/outputImg/how to get video's info.png
    #     print(camera.get(i)) # 内容见 https://www.csdn.net/tags/NtzaYg1sNjE1NjQtYmxvZwO0O0OO0O0O.html