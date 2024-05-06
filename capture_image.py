import io
import cv2
import picamera
import numpy as np
def capture_image():
    #create stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.capture(stream, format='jpeg')
        
    #construct np_array from stream
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    
    #decode image from array
    image = cv2.imdecode(data, 1)
    
    #invert image format from BGR --> RGB
    image = image[:, :, ::-1]
    return image
