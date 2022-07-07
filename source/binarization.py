'''
二值化算法测试与可视化代码
'''

import cv2
import matplotlib.pyplot as plt

def simpleBinary(img): # 简单二值化测试
    ret, thresh1 = cv2.threshold(img, 127, 255, 0)
    ret, thresh2 = cv2.threshold(img, 127, 255, 1)
    ret, thresh3 = cv2.threshold(img, 127, 255, 2)
    ret, thresh4 = cv2.threshold(img, 127, 255, 3)
    ret, thresh5 = cv2.threshold(img, 127, 255, 4)

    titles = ['img', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

def adaptiveBinary(img): # 自适应阈值测试
    # img = cv2.medianBlur(img, 5)

    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 0, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 0, 11, 2)

    titles = ['Original Image', 'Global Thresholding (v = 127)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

def otsuBinary(img):
    # 简单滤波
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    print("Simple:", ret1)
    # Otsu 滤波
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("Otsu's:", ret2)

    plt.figure()
    plt.subplot(221), plt.imshow(img, 'gray'), plt.title("Original")

    plt.subplot(222)
    y, _, _ = plt.hist(img.ravel(), 256)  # .ravel方法将矩阵转化为一维
    plt.vlines(ret1, 0, y.max(), colors="r", ls = '--')
    plt.vlines(ret2, 0, y.max(), colors="g", ls='--')
    plt.title("Hist")

    plt.subplot(223), plt.imshow(th1, 'gray'), plt.title("Simple")
    plt.subplot(224), plt.imshow(th2, 'gray'), plt.title("Otsu's")
    plt.show()

if __name__ == '__main__':
    img = cv2.imread('../images/huiye384.jpg', 0)  # 直接读为灰度图像
    img = cv2.resize(img, (128, 64))  # 将图片zoom到指定大小
    simpleBinary(img)
    adaptiveBinary(img)
    otsuBinary(img)