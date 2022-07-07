'''
视频二值化结果存为二进制文件脚本
'''
import cv2

def videoToFrames(): # 视频提取帧保存到本地
    times = 0
    # 提取视频的频率，每1帧提取一个
    frame_frequency = 1

    # 读取视频帧
    camera = cv2.VideoCapture('../videos/辉夜大小姐2OP 《DADDY _ DADDY _ DO _》 TV Size.mp4')
    # camera = cv2.VideoCapture('../videos/书记舞_辉夜大小姐想让我告白 ED チカっとチカ千花っ♡ - 藤原千花角色歌.mp4')
    while True:
        times = times + 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        # 按照设置间隔存储视频帧
        if times % frame_frequency == 0:
            cv2.imwrite('../output/' + str(times) + '.jpg', image)

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


def videoToBin(): # 视频提取帧
    times = 0
    # 提取视频的频率，每1帧提取一个
    frame_frequency = 3

    # 读取视频帧
    camera = cv2.VideoCapture('../videos/辉夜大小姐2OP 《DADDY _ DADDY _ DO _》 TV Size.mp4')
    # camera = cv2.VideoCapture('../videos/书记舞_辉夜大小姐想让我告白 ED チカっとチカ千花っ♡ - 藤原千花角色歌.mp4')
    with open('../output/video.mmc', 'wb+') as f:
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

                # ret, img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

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

    print('图片提取结束')
    # 释放摄像头设备
    camera.release()

if __name__ == '__main__':
    # videoToFrames()
    videoToBin()