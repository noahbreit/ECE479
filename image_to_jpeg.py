from PIL import Image
def image_to_jpeg(image, label):
    # resize image to (224, 224, 3)
    img_data = Image.fromarray(image)
    img_data = img_data.resize((224, 224), Image.Resampling.LANCZOS)
    img_data.save(f'{label}.jpeg')
    
    return img_data
