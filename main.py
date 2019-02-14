#!/usr/bin/env python3
"""--"""
import cv2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout

cam = cv2.VideoCapture(0)

def getImgBuf():
    frame = cam.read()[-1]
    assert frame is not None
    h, w = frame.shape[:2]
    return frame.tostring(), h, w

buf, h, w = getImgBuf()

# class MainWidget(Widget):
class MainWidget(BoxLayout):
    image = ObjectProperty(None)
    img_texture = ObjectProperty(None)
    def __init__(self):
        super(MainWidget, self).__init__()
        # self.img_texture = Texture.create(size=(w, h), colorfmt='bgr')

    # def on_touch_down(self, touch):
        # pass

    def update_frame(self, dt):
        buf, h, w = getImgBuf()
        self.img_texture = Texture.create(size=(w, h), colorfmt='bgr')
        self.img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')


class CameraApp(App):
    def build(self):
        mw = MainWidget()
        Clock.schedule_interval(mw.update_frame, 1.0 / 60.0)
        return mw


if __name__ == '__main__':
    CameraApp().run()
