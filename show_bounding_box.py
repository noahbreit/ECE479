from PIL import Image
def show_bounding_box(image, bounding_box):
    x1, y1, w, h = bounding_box
    
    # resize image to (224, 224, 3)
    img_data = Image.fromarray(image)
    img_data = img_data.resize((224, 224), Image.Resampling.LANCZOS)
    img_data.save('test.jpeg')
    
    return
