# Picture-defogging：暗通道去雾法


## 算法原理

该算法使用McCarney大气散射模型<img src="https://latex.codecogs.com/svg.image?I(x)=J(x)t(x)&plus;A(1-t(x))" title="I(x)=J(x)t(x)+A(1-t(x))" />，其中<img src="https://latex.codecogs.com/svg.image?I(x)" title="I(x)" />代表待去雾图片、<img src="https://latex.codecogs.com/svg.image?J(x)" title="J(x)" />代表去雾图片、<img src="https://latex.codecogs.com/svg.image?t(x)" title="t(x)" />代表大气折射率、<img src="https://latex.codecogs.com/svg.image?A" title="A" />代表大气光值，则可推断出去雾图片<img src="https://latex.codecogs.com/svg.image?J(x)=(I(x)-A)/t(x)&plus;A" title="J(x)=(I(x)-A)/t(x)+A" />。要想推断出去雾图片，需要计算出大气折射率<img src="https://latex.codecogs.com/svg.image?t(x)" title="t(x)" />和大气光值<img src="https://latex.codecogs.com/svg.image?A" title="A" />，而他们均需要待去雾图片的暗通道。

## 原图
<div align=center>

![image](https://github.com/wk123467/Picture-defogging/blob/master/test.PNG)
</div>

## 暗通道计算方法

1. 计算输入图片所有像素点位置在RGB三通道中的最小值，记为darkMat。例如，某个像素点位置的RGB三通道像素值为[r:34, g:45, b:18]，则该位置选择像素值为18
2. 对darkMat进行最小值滤波(或引导滤波），得到的暗通道示意图如下所示

<div align=center>

![image](https://github.com/wk123467/Picture-defogging/blob/master/暗通道.PNG)
</div>

## 大气光值计算方法

1. 取暗通道前0.1%的像素值位置
2. 找出待去雾图片对应的多个像素值位置
3. 对这些像素值位置取平均，最终得到一个整数A

## 大气折射率计算方法

- 该计算方法为<img src="https://latex.codecogs.com/svg.image?t(x)=1&space;-&space;\omega&space;\space\times(\frac{darkMat}{A})" title="t(x)=1 - \omega \space\times(\frac{darkMat}{A})" />,其中<img src="https://latex.codecogs.com/svg.image?\omega" title="\omega" />为控制去雾程度，因为图片中包含雾可以使图片拥有纵深，更真实。此时得到的大气折射示意图如下所示

<div align=center>

![image](https://github.com/wk123467/Picture-defogging/blob/master/%E5%A4%A7%E6%B0%94%E6%8A%98%E5%B0%84%E5%9B%BE.PNG)
</div>



## 总结

1. 通过大气折射模式的简单变换即可得到去雾图片，方便简洁，而且效果好
2. 算法中实现了两种图像滤波（最小值滤波(左)、引导滤波(右)），得到的结果如下所示。从图中可以观察到引导滤波的效果更好

<div align=center>

![image](https://github.com/wk123467/Picture-defogging/blob/master/%E6%9C%80%E5%B0%8F%E5%80%BC%E6%BB%A4%E6%B3%A2.PNG)
![image](https://github.com/wk123467/Picture-defogging/blob/master/%E5%BC%95%E5%AF%BC%E6%BB%A4%E6%B3%A2.PNG)
</div>

