# Author : Sahil-Pixel
# Date : 31 July 2025
# https://github.com/Sahil-pixel
# https://kivy.org/
# https://www.mathjax.org/
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.graphics.texture import Texture
from kivy.utils import platform
import threading
if platform == 'android':
    from backend.mathjax_render import MathJaxRenderer
    from jnius import autoclass
    Bitmap = autoclass("android.graphics.Bitmap")
    BitmapUtil = autoclass("org.mathjax.BitmapUtil")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")


class MathJaxImage(Image):
    latex = StringProperty("")
    font_size = StringProperty("8px")
    text_color = StringProperty("#000000")
    background_color = StringProperty("#FFFFFF")

    _kr = None

    def __init__(self, **kwargs):
        self._kr = None
        super().__init__(**kwargs)
        self.bind(latex=self.schedule_render)
        self.bind(font_size=self.schedule_render)
        self.bind(text_color=self.schedule_render)
        self.bind(background_color=self.schedule_render)

    def on_kv_post(self, base_widget):
        self.schedule_render()

    def schedule_render(self, *args):
        # Schedule once to avoid multiple calls in one frame
        Clock.unschedule(self.render)
        Clock.schedule_once(self.render, 0)

    def render(self, dt):
        if not self._kr:
            self._kr = MathJaxRenderer(self.on_tex_ready)
        #print("font size ",self.font_size)
        self._kr.set_font_size(self.font_size)
        self._kr.set_text_color(self.text_color)
        self._kr.set_bg_color(self.background_color)
        self._kr.render(self.latex)

    def on_tex_ready(self, bitmap):
        width = bitmap.getWidth()
        height = bitmap.getHeight()

        def convert_pixels():
            # Run this in a thread, doesn't touch Kivy!
            pixels = bytes(BitmapUtil().toPixels(bitmap))

            # Now safely schedule UI update
            def update_texture(dt):
                tex = Texture.create(size=(width, height), colorfmt='rgba')
                tex.blit_buffer(pixels, bufferfmt='ubyte', colorfmt='rgba')
                tex.flip_vertical()
                self.texture = tex
                self.texture_size = list(tex.size)
                self.canvas.ask_update()
                del self._kr

            Clock.schedule_once(update_texture)

        threading.Thread(target=convert_pixels).start()

    def release(self):
        """Clean up Java resources"""
        if self._kr:
            try:
                self._kr.dispose()  # if available
            except Exception:
                pass
            self._kr = None

    def __del__(self):
        self.release()
