'''
视频二值化结果存为二进制文件脚本
'''
import cv2
import os

def videoToFrames(camera, freq=1, folder='frameOutput', types='jpg'): # 视频提取帧保存到本地
    times = 0
    fileName = 0

    # 提取视频的频率，每1帧提取一个
    frame_frequency = freq

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
        print(times)

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


def videoToBin(camera, freq=3, mode='Global', output='video'): # 视频提取帧，输入视频帧，提取间隔（默认3），转换模式（全局、局部）
    times = 0
    # 提取视频的频率，每1帧提取一个
    frame_frequency = freq

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

                if mode == 'Global':
                    _, img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                elif mode == 'Local':
                    img = cv2.adaptiveThreshold(img, 1, cv2.ADAPTIVE_THRESH_MEAN_C, 0, 3, 2)
                    img = binImgReverse(img)

                height = len(img)
                width = len(img[0])
                for i in range(height // 8):
                    for j in range(width):
                        byte = ''
                        for k in range(8):
                            byte += str(img[i * 8 + 7 - k][j])
                        s = bytes([int(byte, 2)])
                        f.write(s)
            print(times)

    print('图片转换结束')
    # 释放摄像头设备
    camera.release()

if __name__ == '__main__':
    # 读取视频帧
    # camera = cv2.VideoCapture('../videos/辉夜大小姐2OP.mp4')
    # camera = cv2.VideoCapture('../videos/书记舞.mp4')
    # camera = cv2.VideoCapture('../videos/辉夜大小姐3ED2.mp4')
    camera = cv2.VideoCapture('../videos/早坂爱lulululu.mp4')

    # videoToFrames(camera, freq=3, folder='shuji', types='jpg')
    videoToBin(camera, mode='Local', output='早坂爱局部')
    # videoToBin(camera, mode='Global', output='早坂爱全局')

    # for i in range(19): # 获取视频的详细参数 见/source/outputImg/how to get video's info.png
    #     print(camera.get(i)) # 内容见 https://www.csdn.net/tags/NtzaYg1sNjE1NjQtYmxvZwO0O0OO0O0O.html