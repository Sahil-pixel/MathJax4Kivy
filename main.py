# Author : Sahil-Pixel
# Date : 31 July 2025
# https://github.com/Sahil-pixel
# https://kivy.org/
# https://www.mathjax.org/
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from mathjax4kivy import MathJaxImage


class ExampleMathJax(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical',padding=10,spacing=5, **kwargs)
        if platform == 'android':
            Clock.schedule_once(self.add_mathjax_widget, 0.2)  # 200ms delay

    def add_mathjax_widget(self, dt):

        tex1 = r'''
            \[ \textbf{MathJax4Kivy supports Python for Android} \]

            \[ \textbf{Author: Sahil-Pixel} \] 

            \[ \textbf{GitHub: https://github.com/Sahil-pixel} \]
            

            \[
            \begin{aligned}
                E &= mc^2 \quad & \text{(Einstein)} \\
                a^2 + b^2 &= c^2 \quad & \text{(Pythagorean theorem)} \\
                \sum_{n=1}^{\infty} \frac{1}{n^2} &= \frac{\pi^2}{6} \\
                \int_0^1 x^2 \, dx &= \frac{1}{3} \\
                \lim_{x \to 0} \frac{\sin x}{x} &= 1 \\
                \binom{n}{k} &= \frac{n!}{k!(n-k)!} \\
                \vec{F} &= m\vec{a}
            \end{aligned}
            \]
            '''


        mjx1 = MathJaxImage(
            latex=tex1,
            font_size="24px",
            text_color="#FFFFFF",
            background_color="#000000"
        )

        self.add_widget(mjx1)
        # For in line math
        #tex2 = r"\[ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} \]"

        tex2 = r"$$ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} $$"

        mjx2 = MathJaxImage(
            latex=tex2,
            font_size="24px",
            text_color="#4B0082",
            background_color="#FFFDD0"
        )
        self.add_widget(mjx2)

        tex3=r'''
        \begin{aligned}
            e^{i\pi} + 1 &= 0 \quad & \text{(Euler's identity)} \\
            \nabla \cdot \vec{E} &= \frac{\rho}{\varepsilon_0} \quad & \text{(Gauss's law)} \\
            f(x) &= \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x - \mu)^2}{2\sigma^2}} \quad & \text{(Normal distribution)} \\
            V &= IR \quad & \text{(Ohm's law)} \\
            A &= \pi r^2 \quad & \text{(Area of a circle)} \\
            PV &= nRT \quad & \text{(Ideal gas law)} \\
            \frac{d}{dx} \left( \sin x \right) &= \cos x \quad & \text{(Derivative of sine)}
        \end{aligned}
        '''

        mjx3 = MathJaxImage(
            latex=tex3,
            font_size="22px",
            text_color="#FF1493",
            background_color="#FFF0F5"
        )
        self.add_widget(mjx3)


class HelloMathApp(App):
    def build(self):
        return ExampleMathJax()


if __name__ == "__main__":
    HelloMathApp().run()
