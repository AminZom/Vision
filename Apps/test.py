from PyQt5 import QtCore, QtGui, QtChart, QtWidgets, uic
from PyQt5.QtChart import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QFileDialog
from surface.inference_model import getPredictions
from circles.CV import find_hough_circles
from PIL import Image
from PIL.ImageQt import ImageQt
import Demo
from Demo import *

import sys
import numpy as np
import cv2
import gc
import atexit
import ctypes
import time

#preds = getPredictions()
camera = None
streamSource = None
isGrab = True
demo = None

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)

class WorkerThread(QThread):
    grabOneFrame = pyqtSignal()
    def run(self):
        global isGrab
        isGrab = True
        while isGrab:
            self.grabOneFrame.emit()
            time.sleep(0.2)
        

class Demo(QtWidgets.QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        uic.loadUi('../UI Files/demo2.ui', self)
        self.setFixedSize(1191, 771)

        self.viewer = PhotoViewer(self)
        self.viewer.photoClicked.connect(self.photoClicked)
        self.viewerLayout.addWidget(self.viewer)
        atexit.register(self.exit_handler)
        
        shadow = QGraphicsDropShadowEffect()  
        shadow.setBlurRadius(-5)
        self.CentrePanel.setGraphicsEffect(shadow) 
    
        self.dashBtn.clicked.connect(lambda: self.changePage("Dashboard"))
        self.workBtn.clicked.connect(lambda: self.changePage("Workspace"))
        self.dataBtn.clicked.connect(lambda: self.changePage("Dataset"))
        self.libBtn.clicked.connect(lambda: self.changePage("Library"))

        self.startBtn.clicked.connect(self.uploadPic)
        self.capImgBtn.clicked.connect(self.captureImage)
        self.connectCamBtn.clicked.connect(self.getFeed)
        self.disconnectCamBtn.clicked.connect(self.stopFeed)
        self.disconnectCamBtn.setVisible(False)

        self.label1 = QLabel("Crazing:")
        self.label1.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label1End = QLabel("--")
        self.label1End.setStyleSheet("color: cyan; font-size: 15px")
        self.label2 = QLabel("Inclusion:")
        self.label2.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label2End = QLabel("--")
        self.label2End.setStyleSheet("color: cyan; font-size: 15px")
        self.label3 = QLabel("Pitted Surface:")
        self.label3.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label3End = QLabel("--")
        self.label3End.setStyleSheet("color: cyan; font-size: 15px")
        self.label4 = QLabel("Patches:")
        self.label4.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label4End = QLabel("--")
        self.label4End.setStyleSheet("color: cyan; font-size: 15px")
        self.label5 = QLabel("Rolled-in Scale:")
        self.label5.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label5End = QLabel("--")
        self.label5End.setStyleSheet("color: cyan; font-size: 15px")
        self.label6 = QLabel("Scratches:")
        self.label6.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        self.label6End = QLabel("--")
        self.label6End.setStyleSheet("color: cyan; font-size: 15px")
        self.gridLayout.addWidget(self.label1, 0, 0)
        self.gridLayout.addWidget(self.label1End, 0, 1)
        self.gridLayout.addWidget(self.label2, 1, 0)
        self.gridLayout.addWidget(self.label2End, 1, 1)
        self.gridLayout.addWidget(self.label3, 2, 0)
        self.gridLayout.addWidget(self.label3End, 2, 1)
        self.gridLayout.addWidget(self.label4, 3, 0)
        self.gridLayout.addWidget(self.label4End, 3, 1)
        self.gridLayout.addWidget(self.label5, 4, 0)
        self.gridLayout.addWidget(self.label5End, 4, 1)
        self.gridLayout.addWidget(self.label6, 5, 0)
        self.gridLayout.addWidget(self.label6End, 5, 1)

        self.hintLabel.setVisible(False)

    def changePage(self, text):
        if text == 'Workspace':
            self.stackedWidget.setCurrentIndex(0)
        elif text == 'Dataset':
            self.stackedWidget.setCurrentIndex(3)
        elif text == 'Library':
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(2)

    def uploadPic(self, text):
        filter = "JPG (*.jpg);;PNG (*.png);;BMP (*.bmp)"
        data_path, _ = QFileDialog.getOpenFileName(None, 'Open File', r"../../Vision Project", filter)
        if(data_path == ""):
            return
        global isGrab
        isGrab = False
        self.viewer.setPhoto(QtGui.QPixmap(data_path))
        self.hintLabel.setVisible(True)
        preds = getPredictions(data_path)
        self.setPredictions(self, preds)

    def setPredictions(self, text, preds):
        self.label1End.setText(str(int(preds[0][0] * 100)) + "%")
        self.label2End.setText(str(int(preds[0][1] * 100)) + "%")
        self.label3End.setText(str(int(preds[0][2] * 100)) + "%")
        self.label4End.setText(str(int(preds[0][3] * 100)) + "%")
        self.label5End.setText(str(int(preds[0][4] * 100)) + "%")
        self.label6End.setText(str(int(preds[0][5] * 100)) + "%")

        predList = []
        predList.append(list((self.label1, self.label1End, int(preds[0][0] * 100))))
        predList.append(list((self.label2, self.label2End, int(preds[0][1] * 100))))
        predList.append(list((self.label3, self.label3End, int(preds[0][2] * 100))))
        predList.append(list((self.label4, self.label4End, int(preds[0][3] * 100))))
        predList.append(list((self.label5, self.label5End, int(preds[0][4] * 100))))
        predList.append(list((self.label6, self.label6End, int(preds[0][5] * 100))))
        sortedPreds = sorted(predList, reverse=True, key=lambda tup: tup[2])

        self.gridLayout.addWidget(sortedPreds[0][0], 0, 0)
        self.gridLayout.addWidget(sortedPreds[0][1], 0, 1)
        self.gridLayout.addWidget(sortedPreds[1][0], 1, 0)
        self.gridLayout.addWidget(sortedPreds[1][1], 1, 1)
        self.gridLayout.addWidget(sortedPreds[2][0], 2, 0)
        self.gridLayout.addWidget(sortedPreds[2][1], 2, 1)
        self.gridLayout.addWidget(sortedPreds[3][0], 3, 0)
        self.gridLayout.addWidget(sortedPreds[3][1], 3, 1)
        self.gridLayout.addWidget(sortedPreds[4][0], 4, 0)
        self.gridLayout.addWidget(sortedPreds[4][1], 4, 1)
        self.gridLayout.addWidget(sortedPreds[5][0], 5, 0)
        self.gridLayout.addWidget(sortedPreds[5][1], 5, 1)

    def pixInfo(self):
        self.viewer.toggleDragMode()

    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))

    def initCamera(self):
        cameraCnt, cameraList = enumCameras()
        if cameraCnt is None:
            return -1
            
        global camera
        camera = cameraList[0]

        nRet = openCamera(camera)
        if ( nRet != 0 ):
            print("openCamera fail.")
            return -1;
            
        streamSourceInfo = GENICAM_StreamSourceInfo()
        streamSourceInfo.channelId = 0
        streamSourceInfo.pCamera = pointer(camera)
        
        global streamSource
        streamSource = pointer(GENICAM_StreamSource())
        nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
        if ( nRet != 0 ):
            print("create StreamSource fail!")
            return -1
        
        trigModeEnumNode = pointer(GENICAM_EnumNode())
        trigModeEnumNodeInfo = GENICAM_EnumNodeInfo() 
        trigModeEnumNodeInfo.pCamera = pointer(camera)
        trigModeEnumNodeInfo.attrName = b"TriggerMode"
        nRet = GENICAM_createEnumNode(byref(trigModeEnumNodeInfo), byref(trigModeEnumNode))
        if ( nRet != 0 ):
            print("create TriggerMode Node fail!")
            streamSource.contents.release(streamSource) 
            return -1
        
        nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
        if ( nRet != 0 ):
            print("set TriggerMode value [Off] fail!")
            trigModeEnumNode.contents.release(trigModeEnumNode)
            streamSource.contents.release(streamSource) 
            return -1
          
        trigModeEnumNode.contents.release(trigModeEnumNode) 
                        
        nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
                                                c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
        if( nRet != 0 ):
            print("startGrabbing fail!")
            streamSource.contents.release(streamSource)   
            return -1
        else:
            print("startGrabbing success!")

        return 0

    def getFeed(self):
        self.connectCamBtn.setVisible(False)
        self.disconnectCamBtn.setVisible(True)
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.finished.connect(self.get_feed_finished)
        self.worker.grabOneFrame.connect(self.grab_one_frame)

    def stopFeed(self):
        print("Stopping thread.")
        global isGrab
        isGrab = False

    def get_feed_finished(self):
        print("Thread finished!")
        self.disconnectCamBtn.setVisible(False)
        self.connectCamBtn.setVisible(True)

    def grab_one_frame(self):
        if(camera == None):
            ctypes.windll.user32.MessageBoxW(0, u"No camera detected!", u"Error", 0)
            return

        self.hintLabel.setVisible(True)
        
        frame = pointer(GENICAM_Frame())
        nRet = streamSource.contents.getFrame(streamSource, byref(frame), c_uint(1000))
        if ( nRet != 0 ):
            print("getFrame fail! Timeout:[1000]ms")
            streamSource.contents.release(streamSource)   
            return -1 
        #else:
            #print("getFrame success BlockId = [" + str(frame.contents.getBlockId(frame)) + "], get frame time: " + str(datetime.datetime.now()))
        
        nRet = frame.contents.valid(frame)
        if ( nRet != 0 ):
            print("frame is invalid!")
            frame.contents.release(frame)
            streamSource.contents.release(streamSource)
            return -1 

        imageParams = IMGCNV_SOpenParam()
        imageParams.dataSize    = frame.contents.getImageSize(frame)
        imageParams.height      = frame.contents.getImageHeight(frame)
        imageParams.width       = frame.contents.getImageWidth(frame)
        imageParams.paddingX    = frame.contents.getImagePaddingX(frame)
        imageParams.paddingY    = frame.contents.getImagePaddingY(frame)
        imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

        imageBuff = frame.contents.getImage(frame)
        userBuff = c_buffer(b'\0', imageParams.dataSize)
        memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)

        frame.contents.release(frame)

        grayByteArray = bytearray(userBuff)
        cvImage = np.array(grayByteArray, dtype=np.uint8).reshape(imageParams.height, imageParams.width)
        #qImg = QImage(cvImage.data, imageParams.height, imageParams.width, 1, QImage.Format_Mono)
        img = Image.fromarray(cvImage)
        if(self.algorithmDropdown.currentIndex() == 0):         #None
            imgPixmap = QtGui.QPixmap.fromImage(ImageQt(img))
        elif(self.algorithmDropdown.currentIndex() == 1):       #Surface Detection
            imgPixmap = QtGui.QPixmap.fromImage(ImageQt(img))
        elif(self.algorithmDropdown.currentIndex() == 2):       #Circle Detection
            img_with_circles, circles_text = find_hough_circles(img, 10, 200, 1, 100, 0.4, 100, 200)
            imgPixmap = QtGui.QPixmap.fromImage(ImageQt(img_with_circles))

        self.viewer.setPhoto(imgPixmap)

    def exit_handler(self):
        print("ENDING")

    def captureImage(self, text):
        global isGrab
        isGrab = False
        nRet = grabOne(camera)
        if( nRet != 0 ):
            print("grabOne fail!")
            streamSource.contents.release(streamSource)   
            return -1      
        else:
            print("trigger time: " + str(datetime.datetime.now()))
        
        frame = pointer(GENICAM_Frame())
        nRet = streamSource.contents.getFrame(streamSource, byref(frame), c_uint(1000))
        if ( nRet != 0 ):
            print("SoftTrigger getFrame fail! timeOut [1000]ms")
            streamSource.contents.release(streamSource)   
            return -1 
        else:
            print("SoftTrigger getFrame success BlockId = " + str(frame.contents.getBlockId(frame))) 
            print("get frame time: " + str(datetime.datetime.now()))   
        
        nRet = frame.contents.valid(frame)
        if ( nRet != 0 ):
            print("frame is invalid!")
            frame.contents.release(frame)
            streamSource.contents.release(streamSource)
            return -1 
        
        imageSize = frame.contents.getImageSize(frame)
        buffAddr = frame.contents.getImage(frame)
        frameBuff = c_buffer(b'\0', imageSize)
        memmove(frameBuff, c_char_p(buffAddr), imageSize)
    
        convertParams = IMGCNV_SOpenParam()
        convertParams.dataSize = imageSize
        convertParams.height = frame.contents.getImageHeight(frame)
        convertParams.width = frame.contents.getImageWidth(frame)
        convertParams.paddingX = frame.contents.getImagePaddingX(frame)
        convertParams.paddingY = frame.contents.getImagePaddingY(frame)
        convertParams.pixelForamt = frame.contents.getImagePixelFormat(frame)
        
        frame.contents.release(frame)
     
        bmpInfoHeader = BITMAPINFOHEADER() 
        bmpFileHeader = BITMAPFILEHEADER()
    
        uRgbQuadLen = 0
        rgbQuad = (RGBQUAD * 256)()
        rgbBuff = c_buffer(b'\0', convertParams.height * convertParams.width * 3)
        
        if convertParams.pixelForamt == EPixelType.gvspPixelMono8:
            for i in range(0, 256):
                rgbQuad[i].rgbBlue = rgbQuad[i].rgbGreen = rgbQuad[i].rgbRed = i;

            uRgbQuadLen = sizeof(RGBQUAD) * 256    
            bmpFileHeader.bfSize = sizeof(bmpFileHeader) + sizeof(bmpInfoHeader) + uRgbQuadLen + convertParams.dataSize
            bmpInfoHeader.biBitCount = 8
        else:
            rgbSize = c_int()
            nRet = IMGCNV_ConvertToBGR24(cast(frameBuff, c_void_p), byref(convertParams), \
                                        cast(rgbBuff, c_void_p), byref(rgbSize))
        
            if ( nRet != 0 ):
                print("image convert fail! errorCode = " + str(nRet))
                streamSource.contents.release(streamSource)
                return -1 
            
            bmpFileHeader.bfSize = sizeof(bmpFileHeader) + sizeof(bmpInfoHeader) + rgbSize.value
            bmpInfoHeader.biBitCount = 24   
        
        bmpFileHeader.bfType = 0x4D42
        bmpFileHeader.bfReserved1 = 0
        bmpFileHeader.bfReserved2 = 0
        bmpFileHeader.bfOffBits = 54 + uRgbQuadLen
        
        bmpInfoHeader.biSize = 40
        bmpInfoHeader.biWidth = convertParams.width
        bmpInfoHeader.biHeight = -convertParams.height
        bmpInfoHeader.biPlanes = 1
        
        bmpInfoHeader.biCompression = 0
        bmpInfoHeader.biSizeImage = 0
        bmpInfoHeader.biXPelsPerMeter = 0
        bmpInfoHeader.biYPelsPerMeter = 0
        bmpInfoHeader.biClrUsed = 0
        bmpInfoHeader.biClrImportant = 0    
        
        fileName = '.\image\image.bmp'
        imageFile = open(fileName, 'wb+') 
        
        imageFile.write(struct.pack('H', bmpFileHeader.bfType))
        imageFile.write(struct.pack('I', bmpFileHeader.bfSize))
        imageFile.write(struct.pack('H', bmpFileHeader.bfReserved1))
        imageFile.write(struct.pack('H', bmpFileHeader.bfReserved2))
        imageFile.write(struct.pack('I', bmpFileHeader.bfOffBits))
        
        imageFile.write(struct.pack('I', bmpInfoHeader.biSize))
        imageFile.write(struct.pack('i', bmpInfoHeader.biWidth))
        imageFile.write(struct.pack('i', bmpInfoHeader.biHeight))
        imageFile.write(struct.pack('H', bmpInfoHeader.biPlanes))
        imageFile.write(struct.pack('H', bmpInfoHeader.biBitCount))
        imageFile.write(struct.pack('I', bmpInfoHeader.biCompression))
        imageFile.write(struct.pack('I', bmpInfoHeader.biSizeImage))
        imageFile.write(struct.pack('i', bmpInfoHeader.biXPelsPerMeter))
        imageFile.write(struct.pack('i', bmpInfoHeader.biYPelsPerMeter))
        imageFile.write(struct.pack('I', bmpInfoHeader.biClrUsed))
        imageFile.write(struct.pack('I', bmpInfoHeader.biClrImportant))    
        
        if convertParams.pixelForamt == EPixelType.gvspPixelMono8:
            for i in range(0, 256):
                imageFile.write(struct.pack('B', rgbQuad[i].rgbBlue)) 
                imageFile.write(struct.pack('B', rgbQuad[i].rgbGreen))   
                imageFile.write(struct.pack('B', rgbQuad[i].rgbRed))           
                imageFile.write(struct.pack('B', rgbQuad[i].rgbReserved))
            
            imageFile.writelines(frameBuff)
        else: 
            imageFile.writelines(rgbBuff)
            
        imageFile.close()
        print("save " + fileName + " success.")
        print("save bmp time: " + str(datetime.datetime.now()))

        self.viewer.setPhoto(QtGui.QPixmap(fileName))
        preds = getPredictions(fileName)
        self.setPredictions(self, preds)
        self.hintLabel.setVisible(True)

    nRet = initCamera()
    if nRet != 0:
        print("Some Error happened!!!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
