from PIL import Image
import os


def resize(dir_path, fixed_width):
    """
    функция пропорционально меняет размер изображения в зависимости от заданной ширины
    :param dir_path: image path
    :param fixed_width: fixed width in pixels
    :return:
    """
    for filename in os.listdir(dir_path):
        img = Image.open(dir_path + '/' + filename)
        width_percent = (fixed_width / float(img.size[0]))
        height_size = int((float(img.size[0]) * float(width_percent)))
        new_image = img.resize((fixed_width, height_size))
        # new_image.show()
        new_image.save(f'resized/{filename[0:2]}.jpg')

