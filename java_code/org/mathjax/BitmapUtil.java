package org.mathjax;

import android.graphics.Bitmap;
import java.nio.ByteBuffer;

public class BitmapUtil {

    public byte[] toPixels(Bitmap bitmap) {
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();

        ByteBuffer buffer = ByteBuffer.allocate(width * height * 4);
        bitmap.copyPixelsToBuffer(buffer);
        bitmap.recycle();

        byte[] bytes = new byte[buffer.capacity()];
        buffer.rewind(); // rewind to read from start
        buffer.get(bytes);

        return bytes;
    }
}
