def detect_and_crop(mtcnn, image):
    if mtcnn.detect_faces(image) == []:
        return None
    
    detection = mtcnn.detect_faces(image)[0]
    box = detection['box']
    
    x1 = box[0]
    y1 = box[1]
    x2 = x1 + box[2]
    y2 = y1 + box[3]
    
    new_x1 = (int)(x1 * 9/10)
    new_y1 = (int)(y1 * 9/10)
    new_x2 = (int)(x2 * 11/10)
    new_y2 = (int)(y2 * 11/10)
    
    width = x2 - x1
    height = y2 - y1
    new_width = new_x2 - new_x1
    new_height = new_y2 - new_y1
    
    cropped_dim = [x1 - new_x1, y1 - new_y1, width, height]
    cropped_image = image[new_y1 : new_y2, new_x1 : new_x2, :]
    
    return cropped_image, cropped_dim
