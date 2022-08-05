import cv2
import numpy as np
from skimage.morphology import disk
import skimage.filters.rank as sfr

#参数
kernel_size = 15
Omega = 0.95

#读取图片
img = cv2.imread("9.PNG")
img = img / 255.0


"""
计算有雾图片的暗通道，可显示暗通道图
1.将每个像素点在RGB三个通道内的最小值找出，设为min_mat
2.设定滤波窗口的大小，对min_mat进行局部滤波操作,获得暗通道dark_mat
"""
def zmMinFilterGray(src, r=7):
    '''''最小值滤波，r是滤波器半径'''
    return cv2.erode(src, np.ones((2 * r - 1, 2 * r - 1)))
def guidedfilter(I, p, r = 81, eps = 0.001):
    '''''引导滤波，直接参考网上的matlab代码'''
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    return m_a * I + m_b
dark_mat = np.min(img, 2)  # 得到暗通道图像
#dark_mat = guidedfilter(dark_mat, zmMinFilterGray(dark_mat, 7))  # 使用引导滤波优化
#dark_mat = zmMinFilterGray(dark_mat, 7)



"""
计算大气光值A
1.取暗通道前0.1%的像素值位置
2.找出原图对应的像素值位置
3.对这个像素值位置取平均，最终得到一个整数
"""

dark_mat_copy = dark_mat.copy()
dark_mat_copy = dark_mat_copy.reshape(-1)  #展开成一维
img_copy = img.copy()
img_copy = img_copy.reshape(-1, 3)       #展开成二维，并且形式为：(像素点位置，三通道信息)


top_pixels_num = int(dark_mat.shape[0] * dark_mat.shape[1] * 0.001)
top_pixels_index = np.argsort(dark_mat_copy)[::-1]    #对所有像素值进行排序
index_of_sort = top_pixels_index[0:top_pixels_num]   #获取最大像素值所在位置

A = img_copy[index_of_sort]
A = np.mean(A, axis=1).mean()   #取平均，获得大气光值整数

"""
计算大气折射率：根据McCarney大气散射模型,可显示大气折射图
T = 1 - w * (min_mat / A)
"""
T = 1 - Omega * (dark_mat / A)
T = np.maximum(T, 0.1)


"""
获取去雾后的图片：J = (I - A) / T + A
"""
T = np.array([T, T, T]).transpose(1, 2, 0)
J = (img - A) / T + A
cv2.imwrite('result.jpg', J)

