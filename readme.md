# Video2Lcd

English|[简体中文](readme_cn.md)

This is a software to convert video to lcd format and its source code based on Python 3. You can use the python script [videoToBin.py](source/videoToBin.py) to simply get the image bin file.

![demo](https://user-images.githubusercontent.com/48848908/178132739-5a8b3d49-e480-42a5-9109-fb3c6784c800.png)

## Structure

```bash
video2lcd/
    ├─images/                     // test input images
    ├─output/                     // output bin files
    ├─Proteus/                    // MCU simulation folder
    │  ├─program/                 // source program based on Keil
    │  └─simulation/              // simulation files based on Proteus
    ├─source/                     // source code folder
    │  ├─outputImg/               // some test images
    ├─tools/                      // two transcoding tools
    │  ├─binHEBING合并bin文件/     // merge bin files
    │  └─Image2Lcd/               // convert images to lcd format
    └─videos/                     // test input videos
```

## Simple use

1. After cloning this repo you should have a python environment not less than 3.7.4. 

2. Then inatall opencv-python.

   ```bash
   pip install opencv-python
   ```

3. If you want to plot results, you should also install matplotlib.

   ```bash
   pip install matplotlib
   ```

4. Use [binarization.py](source/binarization.py) to verify the effectiveness of different algorithms.

   ![simpleBinary](https://user-images.githubusercontent.com/48848908/178133492-decd6c98-fbcb-4af2-9890-cae6baba3084.png)
   ![adaptiveBinary12864-1](https://user-images.githubusercontent.com/48848908/178133409-58f828f8-0e02-4712-abc5-2f0b911e0cf7.png)
   ![otsuBinary12864](https://user-images.githubusercontent.com/48848908/178133497-a54fdd58-7d7d-4761-9f87-0500ad958c08.png)

5. Use [imgToBin.py](source/imgToBin.py) to test the transform method on one image.

6. Use [videoToBin.py](source/videoToBin.py) to simply get the image bin file. 

   We offer two kinds of binarization method: Global & Local, the conversion effect is as shown above.

   We provide parameters to suit different conversion needs:

   ```python
   freq=3,                      # extract frame interval
   transMode='Global'/'Local',  # transform mode
   reverse=False,               # whether the color is reversed
   reOrder=False,               # whether the bytes are in reverse order
   UDFlip=False,                # whether to scan from bottom to top
   RLFlip=False,                # whether to scan from right to left
   scanMode=0(0,1,2,3)          # scanning mode: 
   # 0 horizontal scan; 1 vertical scan; 2 data horizontal, byte vertical; 3 data vertical, byte horizontal
   ```

   When you get the `.bin` file under `/output/`, you can rename it into `.mmc`. Then copy it into `/Proteus/simulation`, add it into the sd card at sd.pdsprj.

## Installation

Go to source code folder

```bash
cd source
```

Create a virtual environment using venv

```bash
python -m venv env
```

Source the virtual environment

Windows:

```bash
cd env/bin
activate
```

Linux:

```bash
source env/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

*p.s.  The graphics window software is under development, the Qt Designer file is `source/simpleUI.ui`.*

---

Todo List：

- [ ]  Develop the corresponding graphics window software.
- [ ]  Support color video generation.

---

coming soon~