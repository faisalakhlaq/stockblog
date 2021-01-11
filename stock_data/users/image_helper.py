from os import path
from pathlib import Path
import imghdr
import secrets
from flask import current_app
from PIL import Image
import imagehash
from werkzeug.utils import secure_filename
from flask_login import current_user

from stock_data.users.models import User


# TODO check how to include more formats in imghdr method
def get_file_format(stream):
    """
    Checks the header of the file and detects the format.
    Method uses allowed imghdr.
    File formats in imghdr are:
    rgb, gif, pbm, pgm, ppm, tiff, rast, xbm, jpeg,bmp,png,webp, exr

    :param stream:
    :returns:
    File format if found in a list of available formats. Else None
    """
    stream.seek(0)
    header = stream.read(512)
    img_format = imghdr.what(None, header)
    if not img_format:
        return None
    return '.' + img_format


def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_user_image(file, user_id=None):
    '''
    Perform a few checks on the image.
    Reduce the size to 125*125 using Pillow.
    Save the user profile image.
    :raises TypeError if a wrong file type is uploaded
    :returns path of the uploaded image
    '''
    # check if there is a file or not
    if not file:
        return None
    # if user does not select file, browser will
    # submit an empty part without filename
    if file.filename == '':
        return None
    if not is_allowed_file(file.filename):
        raise TypeError("This file type is not allowed.\n Allowed types:",
                        current_app.config['ALLOWED_EXTENSIONS'])
    # analyze the file to check if the format
    # is similar to what the image name represents
    detected_format = get_file_format(file.stream)
    file_ext = path.splitext(file.filename)[1]
    if detected_format != file_ext:
        raise TypeError("Strange image! Please choose another image")
    # generate a new name for the image
    image_new_name = generate_image_name(file.filename, user_id=user_id)
    # find the path where the image should be stored
    image_path = get_image_storage_path(image_new_name)
    # reducing the image size
    resized_image = resize_image(file)
    resized_image.save(image_path)
    return image_new_name


def generate_image_name(image_file_name, user_id=None):
    '''
    Generates a random name for the user image and adds user id to the name
    :param image_file_name: name of the file to be changed
    :param user_id: id of the user. Image is named with given id
    :return: a new unique name for the image
    '''
    user_filename = secure_filename(image_file_name)
    random_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(user_filename)
    image_name = random_hex
    # Check if the user exists, otherwise append the
    # next next available id to the image name
    # TODO check only current_user.is_authenticated
    if not current_user or not isinstance(current_user, User) or not current_user.user_id:
        if user_id:
            image_name = image_name + str(user_id) + f_ext
        else:
            image_name = image_name + f_ext
    else:
        image_name = image_name + str(current_user.user_id) + f_ext
    return image_name


def get_image_storage_path(image_file_name):
    # basedir = path.abspath(path.dirname(__file__))
    # file_path = path.join(basedir, app.config['IMAGE_FOLDER'], filename)
    # file.save(file_path)
    picture_path = path.join(current_app.root_path, current_app.config['IMAGE_FOLDER'], image_file_name)
    return picture_path


def resize_image(image_file):
    '''
    resizes the image to 125*125
    @:returns resized image
    '''
    output_size = (125, 125)
    i = Image.open(image_file)
    i.thumbnail(output_size)
    return i


def delete_image(file_name):
    """
    Finds the path of the image. If it exists then deletes it
    :param file_name:
    """
    file_path = Path(get_image_storage_path(file_name))
    if file_path.exists():
        file_path.unlink()


def identical_images(image):
    """
    Compare the given image with the current user profile image.
    :param image: image to be compared with current user image
    :return: True if similar, False if the images are not similar
    """
    # Check if the user image is available or accidentally deleted
    file_path = Path(get_image_storage_path(current_user.image_url))
    if not file_path.exists():
        return False
    # since we resize image before storing, therefore,
    # lets restore the new image and then compare
    resized_image = resize_image(image)
    hash0 = imagehash.average_hash(resized_image)
    hash1 = imagehash.average_hash(Image.open(file_path))
    cutoff = 2
    if hash0 - hash1 < cutoff:
        return True
    else:
        return False
