# -*- codeing = utf-8 -*-
# @Time : 2021/5/9 21:41
# @File ：校内赛识别图形最终版本.py
# @Software : PyCharm
import cv2 as cv


# 查找形状
def detectShape(img):
    # 查找轮廓，cv2.RETR_ExTERNAL=获取外部轮廓点, CHAIN_APPROX_NONE = 得到所有的像素点
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # 循环轮廓，判断每一个形状
    global count
    global objectType
    count = 0
    objectType = None
    for cnt in contours:
        # 获取轮廓面积
        area = cv.contourArea(cnt)
        # 当面积大于1500，代表有形状存在
        if area > 1500:
            # 绘制所有的轮廓并显示出来
            cv.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            # 计算所有轮廓的周长，便于做多边形拟合
            peri = cv.arcLength(cnt, True)
            # 多边形拟合，获取每个形状的边
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            objCor = len(approx)
            # 获取每个形状的x，y，w，h
            x, y, w, h = cv.boundingRect(approx)
            # 计算出边界后，即边数代表形状，如三角形边数=3
            if objCor == 3:
                objectType = "Triangle"
                print("形状是%s,面积是%d" % (objectType, area))
                count += 1
            elif objCor == 4:
                objectType = "Rectangle"
                print("形状是%s,面积是%d" % (objectType, area))
                count += 1
            # 大于4个边的就是五边形
            elif 5 <= objCor < 7:
                objectType = "Pentagon"
                print("形状是%s,面积是%d" % (objectType, area))
                count += 1
            elif objCor == 8:
                objectType = "Circle"
                print("形状是%s,面积是%d" % (objectType, area))
                count += 1
            elif objCor > 8:
                objectType = "Star"
                print("形状是%s,面积是%d" % (objectType, area))
                count += 1
            # 绘制文本时需要绘制在图形附件
            cv.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(
                imgContour,
                objectType,
                (x + (w // 2) - 10, y + (h // 2) - 10),
                cv.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 0, 0),
                2,
            )


if __name__ == "__main__":
    # 调用笔记本内置摄像头，所以参数为0，官方摄像头为1
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    while True:
        # 从摄像头读取图片
        success, img = cap.read()
        # 转换大小
        img = cv.resize(img, (1000, 700))
        # 灰度化
        imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 高斯平滑
        imgBlur = cv.GaussianBlur(imgGray, (7, 7), 1)
        # 边缘检测
        imgCanny = cv.Canny(imgBlur, 200, 200)
        # 膨胀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
        swell = cv.dilate(imgCanny, kernel=kernel)
        # 调用检测函数
        imgContour = img.copy()
        detectShape(swell)
        # 绘制文本
        cv.putText(
            imgContour,
            "%s,%d" % (objectType, count),
            (10, 50),
            cv.FONT_HERSHEY_PLAIN,
            2.0,
            (0, 0, 0),
            2,
        )
        # 若参数delay≤0：表示一直等待按键；
        # 若delay取正整数：表示等待按键的时间，比如cv2.waitKey(100)，就是等待100毫秒
        k = cv.waitKey(100)
        # 保持画面的持续。
        cv.imshow("img", imgContour)
        if k == 27:
            # 通过esc键退出摄像
            cv.destroyAllWindows()
            break

    # 关闭摄像头
    cap.release()
    cv.destroyAllWindows()
