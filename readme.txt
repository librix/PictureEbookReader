# 说明
中文环境具有大部分PDF电子书是图片的集合的特殊性，因而没有适宜的阅读器。
受 supermemo 软件设计 和 Zweitgedächtnis Niklas Luhmanns 知识管理思想启发，作如下假设：
- Pic_PDF 本质是图片，资源管理器 explorer 或否配合各专业软件管理图片最佳。
- 笔记或摘录的本质是该内容对未来时刻可复现的需求：
  - 当我们有一块好的石头，心里的第一反应是放在盒子里面，需要的时刻再拿出来，存储知识和收藏石头一样。
  - 古人传书千年，千年后可复现当年笔迹，不失神韵，直接展示而不必追求文字化；追求文字化的一个方向是可以让机器/软件从中思考，但这个任务对于个人来说太艰巨了，完全可以暂时舍弃。甚至可能迷失在辨别文字和输入法、字库的汪洋。
  - 对于内容而言，只有理解和不理解两类，对于理解的内容，完全是有可能记忆的，不理解的内容完全可以通过重复的专注其中从而获得理解，甚至增加不同的生活阅历后的理解能力也会增强。
  - 假如摘录是抄书的话，为什么不直接拍照？
- 知识管理的核心是专注于知识本身：
  - 当需要厘清概念的时候，我习惯将相同的内容放在一起，前后的逻辑关系组合在一起。其余无关的内容删去。
    - 原文不变的内容是保持不变的；
	- 自己的想法参与到文本之中，可以完全自己“写”出笔记，而不是从书中摘录。
	- 删除无关内容以及留白是为了保持对特定概念思考的专注，一时间思考当前的概念。
  - 为了理解一个概念，有时候会拆分成不同的小概念。或者细分子问题，或进行问题归化。
    - 为了“理解”，是要读原文，因此关键概念在“拆”图和“合”图。
    - 自己有思考，是要“写”笔记，是已经脱离了图/书，仅引用即可。
  - 专注于文本：
    - “递归”的拆分阅读对象，如按目录级别，可拆分到书的最小类别。而这一最小类别仍然有数页不等的说明，每页有段，每段有句，单句组成句群或许不受段落控制，因知识密度不同，或是多段说清了一个内容；
	- 电子屏幕的制约：笔电的大小能单次显示的文字有限，因此要让屏幕一次展示的内容“全面”。
	- 剔除无用的内容：
	  - 如同机器学习前的mining，人类的学习材料经过清洗更有利于集中精神，如果不存在阅读障碍，则不需要清理，甚至不需要这个软件。
	  - 去密码、去水印。
	  - “切边”切去页眉、页脚及四周空白，调整水平或垂直对齐，因此剩下有用的正文。
	  - 加深文字（Gamma校正、高斯锐化等）等图片数据清洗，可以让视觉对比更敏锐。
    - 思考的线性性：
      - 思维敏捷很好，但闪念对于记忆来说很难，材料最好不要逃脱组织材料的线性性。* 我没想好怎么描述，这是管理图片的核心。

# 效果及实现

## 安装
还没学会面向对象，暂时用python写一个思路，有这几个 package 就可以运行。
```
os
shutil
time
clipboard
numpy
cv2
pywin32 
random
```

## 入门
- `BookList.txt` 管理软件读取的图片库。内容是图片所在文件夹路径，一个路径一行，支持子文件夹。
- `复制路径复制.ahk` 定义了 ctrl-4 打开软件，ctrl-shift-c 复制路径。
  - Ctrl-Alt-C in Explorer.exe and IrfanView can copy file url with AHK
  - 资源管理器和IrfanView中Ctrl-Alt-C复制文件路径。
- `main - v0.2.py` 主要思路代码。
- `crop` 示例。

首先需要打开 `复制路径复制.ahk`。

按下 ctrl-4 启动。启动时默认读取剪贴板，如果是图片路径则打开，否则随机打开一张图片库的图。

背后显示控制台，输出一些操作。

- Esc: Exit 退出
- Click: drawing point. 点击画点。
- S/V: Split with Points. 键入S或V，水平或竖向切割图片.
- E: Erase. 删除展示文件（防止误删除，移动到上级0-finished目录下，如果操作错误，可以避免损失，如果已经处理的图片没有用处，可以随时删除。）
- R: Ramdon load a picture from BookList.txt: 从 BookList.txt 中随机加载一张图片。
- H/L:load per/next picture in the same dir. 加载同目录下上/下一文件（非图片闪退）
- J/K (or mouse M-button WheelUp/Down):move up or down in the same pic. 同图片上下移动。
- P: Merge/V-Concat with the next picture. 与下张图片纵向合并（可能闪退）
- O: Open picture with IrfanView. 使用 IrfanView 图片查看器打开（非独立线程）。
- D: Open picture in Explorer selection type. 资源管理器定位当前图片。

# 预处理
- `复制路径复制.ahk` 定义了 ctrl-4 打开软件，可以修改开启的快捷键。
- isOuterInItself 控制切割后的图片保存在哪。同文件夹下，或者另一个地方，我叫它 crop，都是切完的图片。
  - 一般处理 页 的时候，不希望放在同目录下，因为需要向前追赶进度。
    - 当处理一些页后感觉说的是一个概念，可以修改上层目录为该概念名，进行知识组织。
  - 但是在更细读 段 的时候，切割/合并操作变得频繁，更希望放在同目录下操，反复阅读。
- mode 暂无功能，本想用它模拟阅读模式和细读切图模式，但是暂时没有用到。
- IsEnKeyboardLayout 切换成英文输入法的控制，似乎经常失效。
- BookList.txt 管理软件读取的图片库路径。或许可以弄成多个文件表示不同的书架，甚至能解决同一本该放哪个书架的烦恼。




# 效果与实现
程序的基本功能是拆图和并图。文件名以第一次阅读的日期定名，方便后续记忆算法的引入。
程序的基本工作流：Click -> S -> E ...
程序的打断工作流：D查看图片位置、O打开图片、Esc退出。

有几个想法：
- 标签：有些节点图片，作为集合概念，应该标志一个 major 的标签表示重要。作为线性树的一个主叶。
  - 但是引发的问题下几页是子页还是同级下一页。
- 记忆算法：
  - 难度控制
  - 重现期
- 类型: 只需要读 / 具备影响现实能力（转化为行动？） / 习题（比较烦的刷题）


# PictureEbookReader
A python and opencv based picture pdf enhance tool. The main function is to split pictures into different sub-files.

阅读 图片PDF 的图片增强处理工具。 主要功能是分割图片为不同的子文件。

CPU usage is not optimized.

CPU 占用未优化。

The program uses the clipboard extensively. If you use tools such as Ditto, you can see the clipboard changes.

程序大量使用剪贴板。如果使用 Ditto 等工具可以看到剪贴板变化。

## Naming rules 命名规则
NewName:= originName + "." + NewName 

Mulit-NewName:= NewName + "_" + i 

## About path 路径
In order to facilitate management, the export path is fixed.
为了方便管理，导出路径几乎是写死的。

## Next-todo
- Trim Pic
- X: Crop with Points.