# Import Module
import os
import shutil
import time

import clipboard

import numpy as np
import cv2

import win32api  # pywin32 

import random
# [print(i) for i in dir(cv2) if 'EVENT' in i]  
# from ctypes import WinDLL
# import sys

# ############ Output #################
# DllCall("SendMessage", UInt, WinActive("A"), UInt, 80, UInt, 1, UInt, DllCall("LoadKeyboardLayout", Str,"00000409", UInt, 1))

# 程序控制
# isOuterInItself = False   # 切图存放位置， F在别处，T在自身目录下
isOuterInItself = True  # 切图存放在当前图片所在目录

# 随机目录
subjects = []

# readfromTxT_list
with open('./BookList.txt', encoding="utf-8") as f:
    for line in f:
        subjects.append(line)
f.close()
print(subjects)

# 常量
date1 = time.strftime("%Y-%m-%d", time.gmtime())
outerpath = "E:\\2023阅览室\\cropped\\" + date1
if not (os.path.exists(outerpath)):
    os.mkdir(outerpath)



mode = "norm"
Points = []
imgPoints = []


# 测试用
# srcfile = r"...jpg"
IsEnKeyboardLayout = 0




list_of_files = {}
for subject in subjects:
    for (dirpath, dirnames, filenames) in os.walk(subject):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.tif'): 
                if "0-finished" not in dirpath:
                    list_of_files[filename] = os.sep.join([dirpath, filename])

srcfile = clipboard.paste()
if os.path.isfile(srcfile):
    IsSrcFile = 1
else:
    IsSrcFile = 0

def ramdonFile():
    for c in list_of_files.keys():
        a = random.sample(list_of_files.keys(), 1)
        b = a[0]
    return list_of_files[b]


def loadimage(s):
    s = np.fromfile(s, dtype=np.uint8)
    return s


def clearPoint():
    global Points,imgPoints  # ,height 只读，所以不用 global
    Points= []
    imgPoints = []

def y_axis(elem):
    return elem[1]
def x_axis(elem):
    return elem[0]

def split(points):
    global mode  # ,height 只读，所以不用 global

    if len(points) > 1:
        # print(Points)
        if mode == "Hsplit":
            points.sort(key=y_axis)  # key === for x in List: func(x).
        if mode == "Vsplit":
            points.sort(key=x_axis)  # key === for x in List: func(x).

    print(points,height)    
    # spliting image
    
    img_cropped = []
    
    if mode == "Hsplit":
        if len(points) == 1:
            img_cropped_1 = img[0:points[0][1], 0:width]
            img_cropped_2 = img[points[0][1]:height, 0:width]
            img_cropped = [img_cropped_1, img_cropped_2]
        elif len(points) == 2:
            img_cropped_1 = img[0:points[0][1], 0:width]
            img_cropped_2 = img[points[0][1]:points[1][1], 0:width]
            img_cropped_3 = img[points[1][1]:height, 0:width]
            img_cropped = [img_cropped_1, img_cropped_2, img_cropped_3]
        elif len(points) >= 3:
            for i in range(len(points)):
                if i == 0:
                    img_cropped.append(img[0:points[i][1], 0:width])
                    img_cropped.append(img[points[i][1]:points[i + 1][1], 0:width])
                elif i == len(points) - 1:  # last node
                    img_cropped.append(img[points[i][1]:height, 0:width])
                else:
                    img_cropped.append(img[points[i][1]:points[i + 1][1], 0:width])
        else:
            clearPoint()
            print("point out of range. copy whole picture.")
            img_cropped.append(img[0:height, 0:width])
    elif mode == "Vsplit":
        if len(points) == 1:
            img_cropped_1 = img[0:height,0:points[0][0]]
            img_cropped_2 = img[0:height,points[0][0]:width]
            img_cropped = [img_cropped_1,img_cropped_2]
        elif len(points) == 2:
            img_cropped_1 = img[0:height,0:points[0][0]]
            print(img_cropped_1.shape)
            img_cropped_2 = img[0:height,points[0][0]:points[1][0]]
            img_cropped_3 = img[0:height,points[1][0]:width]
            img_cropped = [img_cropped_1, img_cropped_2, img_cropped_3]
        elif len(points) >= 3:
            for i in range(len(points)):
                if i == 0:
                    img_cropped.append(img[0:height,0:points[i][0]])
                    img_cropped.append(img[0:height,points[i][0]:points[i + 1][0]])
                elif i == len(points) - 1:  # last node
                    img_cropped.append(img[0:height,points[i][0]:width])
                else:
                    img_cropped.append(img[0:height,points[i][0]:points[i + 1][0]])
        else:
            clearPoint()
            print("point out of range. copy whole picture.")
            img_cropped.append(img[0:height, 0:width])

    print("------split picture---------")
    # curr_outerpath = os.path.join(outerpath, se)
    # if not (os.path.exists(curr_outerpath)):
    #     os.mkdir(curr_outerpath)
    os.chdir(outerpath)
    # window

    #切割文件名: base.son.....
    base1 = str(os.path.basename(srcfile)[:-4])
    date2 = str(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
    Suffix = str(os.path.basename(srcfile).split(".")[-1])
    outfile = base1 +"_"+ date2

    for id, img_c in enumerate(img_cropped):
        # print(len(enumerate(img_cropped)))
        outfile_i = outfile + "_" + str(id) + "." + Suffix
        cv2.imwrite(outfile_i, img_c)
        print("write pic in ", outfile_i)
    print(os.path.basename(srcfile) + " splits 完毕。")
    # control
    #         k = cv2.waitKey(1) & 0xFF
    #     if k == ord('t'):
    #         mode = "trim"
    #         print("mode change to trim")
    mode = "norm"
    clearPoint()


def crop(points):
    # Cropping image
    if len(points) > 1:
        # print(Points)
        points.sort(key=y_axis)  # key === for x in List: func(x).

    if len(points) == 1:
        # img_cropped = img[0:points[0][1], 0:width]
        pass
    elif len(points) == 2:
        img_cropped = img[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    else:
        clearPoint()
        return

    print("crop picture")
    os.chdir(outerpath)
    # window
    cv2.namedWindow("ROI", cv2.WINDOW_KEEPRATIO)
    cv2.moveWindow("ROI", 40, 40);
    # control
    #         k = cv2.waitKey(1) & 0xFF
    #     if k == ord('t'):
    #         mode = "trim"
    #         print("mode change to trim")
    cv2.imshow("ROI", img_cropped)
    base1 = str(os.path.basename(srcfile)[:-4])
    date2 = str(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
    outfile = base1 +"_crop_" +date2
    Suffix = str(os.path.basename(srcfile).split(".")[-1])

    outfilename = outfile + "."+Suffix
    cv2.imwrite(outfilename, img_cropped)
    print("write pic in ", outfile)
    cv2.waitKey(1500)
    cv2.destroyWindow("ROI")
    global mode
    mode = "norm"
    clearPoint()


def trim(x, y):
    print("trim picture")
    global mode
    mode = "norm"

def click_event(event, x, y, flags, params):
    global mode, Points,imgPoints

    if event == cv2.EVENT_LBUTTONDOWN:
        P1 = (x, y)
        Points.append(P1)
        print('P = ', x, ' ', y)
        imgPoint = (x,y+img_show_start)
        imgPoints.append(imgPoint)
        print("===")
        print('imgPoint = ', imgPoint)

        print("Points = ",Points)
        print("imgPoints",imgPoints)
        print("----------------------")

    elif event == cv2.EVENT_MOUSEMOVE:
        pass

    #     if mode == "crop"
    #         crop(y)
    #         print("crop picture")
    #     else:
    #         trim(x,y)
    #         print("trim picture")
    elif event == cv2.EVENT_LBUTTONUP:
        pass
        if mode == "crop":
            if len(Points) == 2:
                crop(Points)
            # elif len(Points) == 2:
            #     Points[]
        elif mode == "trim":
            trim(x, y)
        else:
            pass
    elif event == cv2.EVENT_MOUSEWHEEL:
        #sign of the flag shows direction of mousewheel
        if flags > 0:
            #scroll up
            print("up")
            curr_page_up()
            
        else:
            #scroll down
            print("down")
            curr_page_down()


def curr_page_up():
    global img_show_start
    if img_show_start >=stepLength:
        img_show_start = img_show_start - stepLength
    else:
        img_show_start = 0

def curr_page_down():
    global img_show_start
    if img_show_start < img_show_start_limit:
        img_show_start += stepLength
        if img_show_start >=img_show_start_limit:
            img_show_start=img_show_start_limit
    else:
        pass


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



def NextFile(s):  # keycode: 39 ->
    file_name = os.path.basename(s)
    dir_path = os.path.dirname(s)
    fileList = os.listdir(dir_path)
    nextIndex = fileList.index(file_name) + 1
    if nextIndex == 0 or nextIndex == len(fileList):
        return None

    next_file = os.path.join(dir_path, fileList[nextIndex])
    clipboard.copy(next_file)
    # clipboard.copy(os.path.basename(next_file).split(".")[0])
    return next_file


def PreFile(s):  # <- 37
    file_name = os.path.basename(s)
    dir_path = os.path.dirname(s)
    fileList = os.listdir(dir_path)
    PreIndex = fileList.index(file_name) - 1
    if PreIndex == -1:
        return None
    prefile = os.path.join(dir_path, fileList[PreIndex])
    clipboard.copy(prefile)
    # clipboard.copy(os.path.basename(prefile).split(".")[0])
    return prefile

def concat_next():
    file_name = os.path.basename(srcfile)
    dir_path = os.path.dirname(srcfile)
    fileList = os.listdir(dir_path)
    nextIndex = fileList.index(file_name) + 1
    if nextIndex == 0 or nextIndex == len(fileList):
        return None
    next_file = os.path.join(dir_path, fileList[nextIndex])
    img1 = cv2.imdecode(loadimage(srcfile), -1)
    img2 = cv2.imdecode(loadimage(next_file), -1)
    if img1.shape[1] == img2.shape[1]:
        if(len(img2.shape)==len(img1.shape)):
            con_img = cv2.vconcat([img1,img2])
            # 降低图片深度!!!!
        elif(len(img2.shape)==3):
            img2t=img2[:,:]            
            con_img = cv2.vconcat([img1,img2t])
        elif(len(img1.shape)==3):
            img2t = np.ones((img2.shape[0],img2.shape[1],3),dtype=np.uint8)*255
            img2t[0:img2.shape[0],0:img2.shape[1],:]=img2[:,:]            
            con_img = cv2.vconcat([img1,img2t])

    elif img1.shape[1] > img2.shape[1]:
        if (len(img2.shape)==3):
            img2t = np.ones((img2.shape[0],img1.shape[1],3),dtype=np.uint8)*255
            print("shape: img2t=",img2t.shape, " img2=", img2.shape)
            img2t[0:img2.shape[0],0:img2.shape[1],:]=img2[:,:,:]
        elif(len(img2.shape)==2):
            img2t = np.ones((img2.shape[0],img1.shape[1]),dtype=np.uint8)*255
            img2t[0:img2.shape[0],0:img2.shape[1]]=img2[:,:]
        con_img = cv2.vconcat([img1,img2t])
    elif img1.shape[1] < img2.shape[1]:
        if (len(img2.shape)==3):
            img1t = np.ones((img1.shape[0],img2.shape[1],3),dtype=np.uint8)*255
            img1t[0:img1.shape[0],0:img1.shape[1],:]=img1[:,:,:]
        elif(len(img2.shape)==2):
            img1t = np.ones((img1.shape[0],img2.shape[1]),dtype=np.uint8)*255
            img1t[0:img1.shape[0],0:img1.shape[1]]=img1[:,:]
        con_img = cv2.vconcat([img1t,img2])
    
    # save
    os.chdir(dir_path)
    base1 = str(os.path.basename(srcfile)[:-4])
    date2 = str(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
    Suffix = str(os.path.basename(srcfile).split(".")[-1])

    outfile = base1 +"_add_"+ date2 + "." + Suffix
    cv2.imwrite(outfile, con_img)
    print("I have concat two pic: ", file_name, " and his next pic ", os.path.basename(next_file) )
    delete_image(srcfile)
    delete_image(next_file)


def openImage(s):
    print(s)
    os.system("\"" + s + "\"")


def delete_image(src):
    global srcfile
    # pass
    # moving and next ...
    dst = os.path.join(os.path.dirname(os.path.dirname(src)), '0-finished')
    # 父目录
    # 的子路径
    if not os.path.exists(dst):
        # cmd mkdir
        os.system("mkdir " + "\"" + dst + "\"")
    srcfile = NextFile(src)
    dstfile = dst
    if os.path.exists(os.path.join(dst,os.path.basename(src))):
        dstfile = os.path.join(dst,os.path.splitext(os.path.basename(src))[0]+"_1"+ os.path.splitext(os.path.basename(src))[1])
    shutil.move(src, dstfile)


def explorer():
    os.system("explorer " + "/select,\"" + srcfile + "\"")
    # dir_path = os.path.dirname(srcfile)
    # os.system("explorer " + "\"" + dir_path + "\"")


if __name__ == '__main__':
    print_hi('World!')
    IsEnKeyboardLayout = 0
    if IsSrcFile:
        current_image = loadimage(srcfile)
    else:
        srcfile = ramdonFile()
    # if (not os.path.isfile(srcfile)) or (not os.path.isdir(srcfile)) or (not (os.path.basename(srcfile).endswith('.jpg') or os.path.basename(srcfile).endswith('.tif'))):
    #     srcfile = ramdonFile()
    # srcfile = clipboard.paste()
    current_image = loadimage(srcfile)
    # "\"" + clipboard.paste() + "\""
    # https://docs.opencv.org/4.x/d8/d6a/group__imgcodecs__flags.html#ga61d9b0126a3e57d9277ac48327799c80

    # img = cv2.imread(srcfile, )
    # img = np.ones((512, 512, 3), np.uint8)

    # img information
    img = cv2.imdecode(current_image, -1)
    dimensions = img.shape
    height = img.shape[0]
    width = img.shape[1]
    # channels = img.shape[2]
    # 图片尺寸太大：an image that is bigger than the screen resolution
    # src: https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga453d42fe4cb60e5723281a89973ee563

    # 2023-01-30 update: 定制窗口大小
    cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    # coordinates, width and height 
    img_show_start=0

    Window_W = 880
    Window_H = 600

    cv2.resizeWindow('image', Window_W, Window_H)


    cv2.moveWindow('image', 20, 20);
    cv2.setMouseCallback('image', click_event)
    
    while 1:
        current_image = loadimage(srcfile)
        if isOuterInItself:
            outerpath = os.path.dirname(srcfile)
        img = cv2.imdecode(current_image, -1)
        # 更新图像信息，因为 slipt 出错
        height = img.shape[0]
        width = img.shape[1]
        ScreenSize = cv2.getWindowImageRect('image')
        # print(ScreenSize)
        _,_,Window_W,Window_H = ScreenSize

        R_H=int(height *  (Window_W / width ))
        if R_H < 600:
            Window_H = R_H
            cv2.resizeWindow('image', Window_W, Window_H)
        else:
            Window_H = 600
            cv2.resizeWindow('image', Window_W, Window_H)

        stepLength = int(Window_H / (Window_W / width )) #一次滑动图片大小
        img_show_start_limit = height - stepLength # 图片起点 in [0，图片总长-窗口长度]

        # 创建拷贝，防止修改 源图片  
        img_cir=img.copy()
        if Points: # 在拷贝上绘制点
            for i in imgPoints:
                img_cir = cv2.circle(img_cir, i, 10, (60, 175, 180), -1)

        img_cir_show=img_cir[img_show_start:img_show_start+stepLength,0:width] # 新建图片框
        cv2.imshow('image', img_cir_show)
        cv2.setWindowTitle( 'image', str(os.path.basename(srcfile)) ) #?
        if not IsEnKeyboardLayout:  # if 0: 不成功。return 0 成功。 
            print("change to En LoadKeyboardLayout")
            win32api.LoadKeyboardLayout("00000409", 1)
            IsEnKeyboardLayout = 1
        k = cv2.waitKey(1) & 0xFF
        if k == ord('t'):
            mode = "trim"
            print("mode change to trim")
        elif k == ord('x'):
            print("mode change to crop")
            mode = "crop"
            crop(imgPoints)
        elif k == ord('n'):
            print("mode quick to normal")
            mode = "norm"
        elif k == ord('s'):
            print("mode change to split")
            mode = "Hsplit"
            split(imgPoints)
        elif k == ord('v'):
            print("mode change to split")
            mode = "Vsplit"
            split(imgPoints)
        elif k == ord('q'):
            clearPoint()
            print("clean Pointer")
        elif k == ord('l'):
            clearPoint()
            print("--->")
            srcfile = NextFile(srcfile)
            img_show_start=0
            IsEnKeyboardLayout = 0
        elif k == ord('h'):
            clearPoint()
            srcfile = PreFile(srcfile) 
            img_show_start=0
            print("<---")
            IsEnKeyboardLayout = 0
        elif k == ord('r'):
            clearPoint()
            srcfile = ramdonFile()         
            img_show_start=0
            print("随机打开一张图")
        elif k == ord('j'):
            curr_page_down()
        elif k == ord('k'):
            curr_page_up()
        elif k == ord('o'):
            openImage(srcfile)
        elif k == ord('p'):
            concat_next()
            srcfile = PreFile(srcfile)
        elif k == ord('d'):
            explorer()
        elif k == ord('e'):
            clearPoint()
            print("已完成：" + os.path.basename(srcfile))
            delete_image(srcfile)
            IsEnKeyboardLayout = 0
            img_show_start=0
        elif k == 27:
            break
        # else:
        #     print(cv2.waitKeyEx())

    # cv2.waitKey(0)  # wait for a key to be pressed to exit
    cv2.destroyAllWindows()  # close the window