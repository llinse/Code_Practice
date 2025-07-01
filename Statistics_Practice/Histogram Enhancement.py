import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *


# 获取局部均值和方差
def part_function(image, size):
    pad = floor(size/2)  # 原图片需要填充的区域
    new_image = np.pad(image, ((pad, pad), (pad, pad)), 'constant')  # 填充后的新图片
    sigma = np.zeros(image.shape)   # 储存局部方差
    mean = np.zeros(image.shape)    # 储存局部均值
    h = image.shape[0]
    w = image.shape[1]
    for i in range(abs(h)):
        for j in range(abs(w)):
            sub_domain = new_image[i:i + 2 * pad, j: j + 2 * pad]
            # 局部直方图
            # image_hist(sub_domain)
            element = np.array(sub_domain.flatten())  # 邻域内所有元素
            local_mean = np.mean(element)    # 局部均值
            mean[i, j] = local_mean
            # sigma[i, j] = sum((element - local_mean) ** 2) / (size ** 2)   # 局部方差
            sigma[i, j] = sqrt(np.var(element))
    return sigma, mean


# 全局直方图
def image_hist(img):
    H = img.shape[0]
    W = img.shape[1]
    hr = np.zeros(256)  # 原始直方图信息
    pr = np.zeros(256)  # 原始图片的概率
    for row in range(H):
        for col in range(W):
            hr[img[row, col]] += 1
    for i in range(256):
        pr[i] = hr[i] / (H * W)
    plt.plot(pr)
    plt.xlim([0, 256])
    plt.show()


# 图片增强
def strengthen(m_g, s_g, mean, sigma, image, E, k_0, k_1, k_2):
    h = image.shape[0]
    w = image.shape[1]
    for i in range(abs(h)):
        for j in range(abs(w)):
            if mean[i, j] <= k_0 * m_g:
                if sigma[i, j] <= k_2 * s_g and sigma[i, j] >= k_1 * s_g:
                    image[i, j] = E * image[i, j]
    return image


# 读取图片
img = cv2.imread('实验2.tif', 0)   # 这里需要指定一个 img_path
local_s, local_m = part_function(img, 1)
print('局部均值：',local_m)
print('局部方差',local_s)
new = strengthen(128.1, sqrt(5671.9), local_m, local_s, img, 4.0, 0.4, 0.02, 0.4)

# plt.hist(new.ravel(), 256, [0, 256])
# plt.show()
cv2.imshow('new_img', new)
cv2.waitKey()
