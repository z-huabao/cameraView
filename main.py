#!/usr/bin/env python3
"""--"""
import os, sys
import datetime
import numpy as np
import img_tools as imt

from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, \
        StringProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.graphics.texture import Texture
# from kivy.graphics.transformation import Matrix

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
# from kivy.uix.dropdown import DropDown

# 设置支持中文字体
Config.set('kivy', 'default_font', [ 'msgothic', './simhei.ttf'])

SAVE_DIR = sys.argv[1] if len(sys.argv) > 1 else './images'
if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)


class ImScatter(Scatter):
    double_tap_scale = NumericProperty(3)
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.scale != 1 or self.pos != (0, 0):
                self.scale = 1.
                self.pos = (0, 0)
            else:
                size = Vector(self.size)
                pos = Vector(touch.x, touch.y)
                self.pos = (size / 2 - pos) * self.double_tap_scale
                self.scale = self.double_tap_scale
            return True
        else:
            return super(ImScatter, self).on_touch_down(touch)

class MainWidget(BoxLayout):
    cam = ObjectProperty(None)
    img_texture = ObjectProperty()
    cam_ids = ListProperty()
    cam_id = StringProperty()
    resolution_init = StringProperty("")

    img_widget = ObjectProperty()
    # image = ObjectProperty(None)
    def __init__(self):
        super(MainWidget, self).__init__()
        self.frame = None
        self.list_cameras(None)

    def open_camera(self, id_):
        """ id_: string, split from /dev/video* """
        self.resolution_init = ""
        if id_ != self.cam_id:
            self.cam_id = id_
            self.cam = imt.Camera(id_)
            self.resolution_init = "1280x960"

    def list_cameras(self, dt):
        """ auto detect camera devices and refresh to spinner """
        self.cam_ids = sorted(f[5:] for f in os.listdir('/dev/') if 'video' == f[:5])
        if self.cam is None and len(self.cam_ids):
            self.open_camera(self.cam_ids[-1])

    def update_slider_value(self, slider):
        value = self.cam.get(slider.text)
        if value is not None:
            value = min(value, 1)
            value = max(value, 0)
            slider.value = value

    def update_frame(self, dt):
        if self.cam:
            self.frame = self.cam.read()
            if self.frame is not None:
                # print(self.img_widget.size)
                h, w = self.frame.shape[:2]
                # print(h, w)
                self.img_texture = Texture.create(size=(w, h), colorfmt='bgr')
                self.img_texture.blit_buffer(self.frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')

    def save(self):
        if self.frame is not None:
            white_frame = np.zeros_like(self.frame) + 255
            self.img_texture.blit_buffer(white_frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')

            out_file = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
            out_file = os.path.join(SAVE_DIR, out_file)
            print("Out file to: %s" % out_file)
            imt.save(out_file, self.frame)
        else:
            pass

class CameraApp(App):
    def build(self):
        mw = MainWidget()
        Clock.schedule_interval(mw.update_frame, 1.0 / 60.0)
        Clock.schedule_interval(mw.list_cameras, 2)
        return mw


if __name__ == '__main__':
    CameraApp().run()
