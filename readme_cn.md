# Video2Lcd

[English](readme.md)|简体中文

这是一个将视频转换为lcd格式的软件及其基于Python 3的源代码。您可以使用python脚本[videoToBin.py](source/videoToBin.py)简单地得到转换后的bin镜像文件。

![demo](https://user-images.githubusercontent.com/48848908/178132739-5a8b3d49-e480-42a5-9109-fb3c6784c800.png)

## 仓库结构

```bash
video2lcd/
    ├─images/                     // 测试输入转换的图片
    ├─output/                     // 输出bin文件的文件夹
    ├─Proteus/                    // 单片机仿真文件夹
    │  ├─program/                 // 用Keil开发的单片机源程序
    │  └─simulation/              // Proteus仿真文件
    ├─source/                     // 源代码文件夹
    │  ├─outputImg/               // 一些测试输出的图片
    ├─tools/                      // 两个第三方转码软件
    │  ├─binHEBING合并bin文件/     // 合并bin文件的软件
    │  └─Image2Lcd/               // 把图片转换为lcd格式的软件
    └─videos/                     // 测试输入的视频
```

## 简单使用

1. 克隆这个仓库后，你电脑上应该有一个不低于 3.7.4 的 python 环境。

2. 安装opencv-python第三方库。

   ```bash
   pip install opencv-python
   ```

3. 如果要绘制结果，还应该安装 matplotlib。

   ```bash
   pip install matplotlib
   ```

4. 使用 [binarization.py](source/binarization.py) 来验证不同算法的有效性。

   ![simpleBinary](https://user-images.githubusercontent.com/48848908/178133492-decd6c98-fbcb-4af2-9890-cae6baba3084.png)

   ![adaptiveBinary12864-1](https://user-images.githubusercontent.com/48848908/178133409-58f828f8-0e02-4712-abc5-2f0b911e0cf7.png)
   ![otsuBinary12864](https://user-images.githubusercontent.com/48848908/178133497-a54fdd58-7d7d-4761-9f87-0500ad958c08.png)

5. 使用 [imgToBin.py](source/imgToBin.py) 在单张图像上测试转换。

6. 使用 [videoToBin.py](source/videoToBin.py) 简单地获得转换后的镜像 bin 文件。

   我们提供两种二值化方法：Global & Local，转换效果如上图。

   我们提供参数以满足不同的转换需求：

   ```python
   freq=3,                      # 提取帧间隔
   transMode='Global'/'Local',  # 变换模式
   reverse=False,               # 颜色是否反转
   reOrder=False,               # 字节是否倒序
   UDFlip=False,                # 是否从下往上扫描
   RLFlip=False,                # 是否从右向左扫描
   scanMode=0(0,1,2,3)          # 扫描模式：
   #0 水平扫描； 1 垂直扫描； 2 数据水平，字节垂直； 3 数据垂直，字节水平
   ```

   当你得到 `/output/` 下的 `.bin` 文件时，你可以将它重命名为 `.mmc`。 然后将其复制到`/Proteus/simulation`，添加到sd.pdsprj工程的sd卡中。

## 完整安装

转到源代码文件夹

```bash
cd source
```

使用 venv 创建虚拟环境

```bash
python -m venv env
```

启动虚拟环境

Windows:

```bash
cd env/bin
activate
```

Linux:

```bash
source env/bin/activate
```

使用包管理器 [pip](https://pip.pypa.io/en/stable/) 来安装需要的包。

```bash
pip install -r requirements.txt
```

*p.s.  图形窗口软件正在开发中，Qt Designer文件为`source/simpleUI.ui`。*

---

Todo List：

- [ ] 开发相应的图形窗口软件。
- [ ] 支持彩色视频生成。

---

敬请期待~