# Author : Sahil-Pixel
# Date : 30 July 2025
# https://github.com/Sahil-pixel
# https://kivy.org/
# https://www.mathjax.org/

from jnius import autoclass, PythonJavaClass, java_method, cast
from kivy.graphics.texture import Texture
from android.runnable import run_on_ui_thread

# Java classes
MathJaxRendererJava = autoclass("org.mathjax.MathJaxRenderer")
#Bitmap = autoclass("android.graphics.Bitmap")
PythonActivity = autoclass("org.kivy.android.PythonActivity")
JavaString = autoclass("java.lang.String")

# Callback interface


class RenderCallback(PythonJavaClass):
    __javainterfaces__ = ['org/mathjax/MathJaxRenderer$RenderCallback']
    __javacontext__ = 'app'

    def __init__(self, callback_fn):
        super().__init__()
        self.callback_fn = callback_fn

    @java_method('(Landroid/graphics/Bitmap;)V')
    def onRendered(self, bitmap):
        self.callback_fn(bitmap)


class MathJaxRenderer:
    def __init__(self, callback_fn):
        context = PythonActivity.mActivity
        self.callback = RenderCallback(callback_fn)
        self.renderer = MathJaxRendererJava(context, self.callback)

    # Core render method
    def _render(self, latex):
        jstr = JavaString(latex.strip().replace("\n", " "))
        self.renderer.renderLatex(jstr)
        # self.renderer.renderNow()
        # self.renderer.measureHtmlContent()

    # ========== Setters ==========
    def render(self, latex):
        return self._render(latex)

    def render_now(self): self.renderer.renderNow()

    def measure_html_content(self): self.renderer.measureHtmlContent()

    def set_width(self, w=512): self.renderer.setWidth(w)

    def set_height(self, h=512): self.renderer.setHeight(h)

    def set_font_size(self, size="8px"): self.renderer.setFontSize(size)

    def set_text_color(
        self, color="#0000ff"): self.renderer.setTextColor(color)

    def set_bg_color(self, color="#ffffff"): self.renderer.setBgColor(color)

    def set_padding(self, padding="2px"): self.renderer.setPadding(padding)

    def set_padding_body(
        self, padding="0"): self.renderer.setPaddingBody(padding)

    def set_margin_body(self, margin="0"): self.renderer.setMarginBody(margin)

    def set_justify(
        self, justify="flex-start"): self.renderer.setJustify(justify)

    def set_align(self, align="flex-start"): self.renderer.setAlign(align)

    def set_html_height(
        self, height="100vh"): self.renderer.setHtmlHeight(height)

    def set_html_width(self, width="100vw"): self.renderer.setHtmlWidth(width)

    def set_custom_math_style(
        self, style=""): self.renderer.setCustomMathStyle(style)

    def set_font_family(
        self, family="sans-serif"): self.renderer.setFontFamily(family)

    # ========== Getters ==========

    def get_width(self): return self.renderer.getWidth()
    def get_height(self): return self.renderer.getHeight()
    def get_font_size(self): return self.renderer.getFontSize()
    def get_text_color(self): return self.renderer.getTextColor()
    def get_bg_color(self): return self.renderer.getBgColor()
    def get_padding(self): return self.renderer.getPadding()
    def get_padding_body(self): return self.renderer.getPaddingBody()
    def get_margin_body(self): return self.renderer.getMarginBody()
    def get_justify(self): return self.renderer.getJustify()
    def get_align(self): return self.renderer.getAlign()
    def get_html_height(self): return self.renderer.getHtmlHeight()
    def get_html_width(self): return self.renderer.getHtmlWidth()
    def get_custom_math_style(self): return self.renderer.getCustomMathStyle()
    def get_font_family(self): return self.renderer.getFontFamily()
    def get_latex(self): return self.renderer.getLatex()
    def is_page_loaded(self): return self.renderer.isPageLoaded()
