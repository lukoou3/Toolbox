from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import aiohttp
import os

from util.asyncUtil import addToLoop, headers
from util.util import makeMd5

cacheFolder = "cache/imgs"
def checkOneFolder(folderName:str):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    def _check(func):
        def _exec(*args):
            try:
                func(*args)
            except Exception as e:
                print(e)
        return _exec
    return _check

## 对<img src=1.jpg>的初步探索。
# 暂只接受http(s)和本地目录。
class PicLabel(QLabel):

    def __init__(self,parent=None,src=None, width=200, height=200, pixMask=None):
        super().__init__(parent)

        self.src = None
        self.width = width
        self.height = height

        self.pixMask = None
        if pixMask:
            self.pixMask = pixMask
        if src:
            self.setSrc(src)

        if self.width:
            self.setMaximumSize(self.width, self.height)
            self.setMinimumSize(self.width, self.height)

    @checkOneFolder(cacheFolder)
    def setSrc(self, src):
        src = str(src)
        if 'http' in src or 'https' in src:
            cacheList = os.listdir(cacheFolder)

            name = makeMd5(src)
            localSrc = cacheFolder+'/'+name
            if name in cacheList:
                self.setSrc(localSrc)
                self.src = localSrc
                return

            self.loadImg(src,name)
        else:
            self.src = src
            pix = QPixmap(src)
            pix.load(src)
            pix = pix.scaled(self.width, self.height)
            # mask需要与pix是相同大小。
            if self.pixMask:
                mask = QPixmap(self.pixMask)
                mask = mask.scaled(self.width, self.height)
                pix.setMask(mask.createHeuristicMask())

            self.setPixmap(pix)

    def getSrc(self):
        """返回该图片的地址。"""
        return self.src

    @addToLoop
    async def loadImg(self,src,name):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(src,headers=headers,timeout=60) as response:
                    if response.status == 200:
                        image_content = await response.read()
                    else:
                        raise aiohttp.ClientError()
        except Exception as e:
            print(e)
            return

        width = self.width
        height = self.height

        pic = QPixmap()
        pic.loadFromData(image_content)
        localSrc = cacheFolder + '/' + name
        pic.save(localSrc, 'jpg')
        pic = pic.scaled(width, height)

        self.src = localSrc

        # 上遮罩。
        if self.pixMask:
            mask = QPixmap()
            mask.load(self.pixMask)
            mask = mask.scaled(width, height)

            pic.setMask(mask.createHeuristicMask())

        self.setPixmap(pic)