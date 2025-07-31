package org.mathjax;

import java.io.File;
import java.io.FileOutputStream;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.FrameLayout;
import android.webkit.WebView;
import android.webkit.WebViewClient;

// Author : Sahil-Pixel
// Date : 31 July 2025
// https://github.com/Sahil-pixel
// https://kivy.org/
// https://www.mathjax.org/

public class MathJaxRenderer {
    private static final String TAG = "MathJaxRenderer";
    private Context context;
    private WebView webView;
    private FrameLayout frameLayout;
    private Handler handler;
    private String latex;
    private RenderCallback callback;
    private int width = 512;
    private int height = 512;
    private boolean pageLoaded = false;

    private String fontSize = "8px";
    private String textColor = "#000000";
    private String bgColor = "#ffffff";
    private String padding = "2px";
    private String paddingBody = "0";
    private String marginBody = "0";
    private String customMathStyle = "";
    private String fontFamily = "sans-serif";

    public interface RenderCallback {
        void onRendered(Bitmap bitmap);
    }

    public MathJaxRenderer(Context ctx, RenderCallback cb) {
        this.context = ctx;
        this.callback = cb;
        this.handler = new Handler(Looper.getMainLooper());
        Log.d(TAG, "Initializing MathJaxRenderer...");

        handler.post(() -> {
            webView = new WebView(context);
            webView.getSettings().setJavaScriptEnabled(true);
            webView.setBackgroundColor(0xFFFFFFFF);
            webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
            webView.setWebViewClient(new WebViewClient() {
                public void onPageFinished(WebView view, String url) {
                    pageLoaded = true;
                    measureHtmlContent();
                }
            });

            frameLayout = new FrameLayout(context);
            FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(width, height);
            frameLayout.addView(webView, params);
        });
    }

    public void renderLatex(String latexStr) {
        this.latex = latexStr;

        String content = "<!DOCTYPE html><html><head>" +
            "<meta charset='utf-8'>" +
            "<meta name='viewport' content='width=device-width, initial-scale=1'>" +

            // MathJax config (MUST come before script include)
            "<script>" +
            "  window.MathJax = {" +
            "    tex: {" +
            "      inlineMath: [['\\\\(', '\\\\)']]," +
            "      displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']]" +
            "    }," +
            "    svg: { fontCache: 'global' }" +
            "  };" +
            "</script>" +

            // Load MathJax
            "<script src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js'></script>" +

            "<style>" +
            "  html, body { margin:0; padding:0; background:" + bgColor + "; display:flex; justify-content:center; align-items:center; height:100vh; }" +
            "  #wrapper { padding:" + padding + "; display:inline-block; background:" + bgColor + "; }" +
            "  #math { font-size:" + fontSize + "; color:" + textColor + "; font-family:" + fontFamily + ";" + customMathStyle + " }" +
            "</style>" +

            "</head><body>" +
            "<div id='wrapper'><div id='math'>" + latex + "</div></div>" +

            "<script>" +
            "  MathJax.typesetPromise().then(function() {" +
            "    if (window.MathBridge) window.MathBridge.onRendered();" +
            "  });" +
            "</script>" +
            "</body></html>";

        handler.post(() -> {
            pageLoaded = false;
            webView.loadDataWithBaseURL(null, content, "text/html", "utf-8", null);
        });
    }

    public void measureHtmlContent() {
        handler.post(() -> {
            webView.evaluateJavascript(
                "(function() {" +
                "  var el = document.getElementById('math');" +
                "  if (!el) return '0,0';" +
                "  var rect = el.getBoundingClientRect();" +
                "  return Math.ceil(rect.width) + ',' + Math.ceil(rect.height);" +
                "})()",
                value -> {
                    try {
                        value = value.replace("\"", "");
                        String[] parts = value.split(",");
                        if (parts.length < 2) throw new IllegalArgumentException("Invalid size: " + value);
                        int cssWidth = Integer.parseInt(parts[0]);
                        int cssHeight = Integer.parseInt(parts[1]);

                        DisplayMetrics metrics = context.getResources().getDisplayMetrics();
                        int androidWidth = (int) Math.ceil(cssWidth * metrics.density);
                        int androidHeight = (int) Math.ceil(cssHeight * metrics.density);

                        this.width = Math.max(1, androidWidth);
                        this.height = Math.max(1, androidHeight);

                        FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(width, height);
                        webView.setLayoutParams(params);
                        frameLayout.measure(
                            View.MeasureSpec.makeMeasureSpec(width, View.MeasureSpec.EXACTLY),
                            View.MeasureSpec.makeMeasureSpec(height, View.MeasureSpec.EXACTLY));
                        frameLayout.layout(0, 0, width, height);
                        frameLayout.invalidate();

                        renderNow();

                    } catch (Exception e) {
                        Log.e(TAG, "Failed to parse size: " + value, e);
                    }
                }
            );
        });
    }

    public void renderNow() {
        handler.postDelayed(() -> {
            if (!pageLoaded) {
                Log.d(TAG, "Waiting for page to load...");
                return;
            }
            Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(bitmap);
            drawNow(canvas);
            if (callback != null) {
                callback.onRendered(bitmap);
            }
        }, 100);
    }

    public void drawNow(Canvas canvas) {
        frameLayout.draw(canvas);
        frameLayout.invalidate();
    }

    public void saveBitmapToJpg(Bitmap bitmap, String filename) {
        try {
            File dir = new File(Environment.getExternalStorageDirectory(), "MathJaxDebug");
            if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, filename + ".jpg");
            FileOutputStream out = new FileOutputStream(file);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();
            Log.d(TAG, "Saved image to: " + file.getAbsolutePath());
        } catch (Exception e) {
            Log.e(TAG, "Failed to save bitmap", e);
        }
    }

    // Getters and Setters...

    public int getWidth() { return width; }
    public void setWidth(int width) { this.width = width; }

    public int getHeight() { return height; }
    public void setHeight(int height) { this.height = height; }

    public String getFontSize() { return fontSize; }
    public void setFontSize(String fontSize) { this.fontSize = fontSize; }

    public String getTextColor() { return textColor; }
    public void setTextColor(String textColor) { this.textColor = textColor; }

    public String getBgColor() { return bgColor; }
    public void setBgColor(String bgColor) { this.bgColor = bgColor; }

    public String getPadding() { return padding; }
    public void setPadding(String padding) { this.padding = padding; }

    public String getPaddingBody() { return paddingBody; }
    public void setPaddingBody(String paddingBody) { this.paddingBody = paddingBody; }

    public String getMarginBody() { return marginBody; }
    public void setMarginBody(String marginBody) { this.marginBody = marginBody; }

    public String getCustomMathStyle() { return customMathStyle; }
    public void setCustomMathStyle(String customMathStyle) { this.customMathStyle = customMathStyle; }

    public String getFontFamily() { return fontFamily; }
    public void setFontFamily(String fontFamily) { this.fontFamily = fontFamily; }

    public String getLatex() { return latex; }
    public void setLatex(String latex) { this.latex = latex; }

    public boolean isPageLoaded() { return pageLoaded; }
}
