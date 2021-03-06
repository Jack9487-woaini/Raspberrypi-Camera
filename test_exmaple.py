import pygame
import pygame.camera
from pygame.locals import *

pygame.init() # 初始化pygame
pygame.camera.init() # 初始化相機模組

class Capture(object):
    def __init__(self):
        self.size = (640,480) # 大小為 640 x 480
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0) # 設置視窗大小

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras() # 搜尋可使用的相機裝置並且放入list
        if not self.clist: # 搜尋不到可使用的相機裝時
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size) # 設置欲啟用的相機，為相機list的第一個
        self.cam.start() # 啟動該相機

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display) # 設置畫布大小，並且把畫布設置在self.display這個視窗上 

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()
a = Capture()
a.main()
