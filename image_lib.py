'''
Authors: Mahenur Master, Nisharg Patel, Sneha Malhotra, Siddharth Patel
Library of useful functions for working with images.
'''
import requests
import ctypes
import os

def main():
    image_url = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg'
    image_data = download_image(image_url)
    
    if image_data:
        image_path = r'C:\temp\kitty.jpg'
        if save_image_file(image_data, image_path):
            set_desktop_background_image(image_path)
    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    print(f'Initiating download from {image_url}...', end='')
    response = requests.get(image_url)

    if response.status_code == 200:
        print('downloaded successfully')
        return response.content
    else:
        print('download failed')
        print(f'Status code: {response.status_code} ({response.reason})')     
        return None

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful
    """
    directory = os.path.dirname(image_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
        print(f"Saving image to {image_path}...", end='')
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        print("save completed")
        return True
    except IOError as e:
        print(f'save failed: {e}')
        return False

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful        

    References:
        https://stackoverflow.com/questions/53878508/change-windows-10-background-in-python-3
        https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
    """
    print(f"Applying {image_path} as desktop wallpaper...", end='')
    SPI_SETDESKWALLPAPER = 20
    try:
        if ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3):
            print("wallpaper applied successfully")
            return True
        else:
            print("wallpaper application failed")
    except Exception as e:
        print(f'application failed: {e}')
    return False

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    scaling_factor = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_dimensions = (int(image_size[0] * scaling_factor), int(image_size[1] * scaling_factor))
    return new_dimensions

if __name__ == '__main__':
    main()
