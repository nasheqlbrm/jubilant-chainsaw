from PIL import Image
import pytesseract

def split_image(image_filepath):
    # Open the image containing two pages side by side
    image = Image.open(image_filepath)  # Replace 'your_input_image.jpg' with your image file path
    
    # Get the dimensions of the original image
    width, height = image.size
    
    # Calculate the width of each page (assuming they are of equal width)
    page_width = width // 2
    
    # Crop the left page
    left_page = image.crop((0, 0, page_width, height))
    
    # Crop the right page
    right_page = image.crop((page_width, 0, width, height))

    return left_page, right_page

def split_left_right(input_path, output_path):
    """
    Take a path with a bunch of images. Splits them down the middle
    then saves the left and right image with extension ...-02.jpg
    and ...-01.jpg. Here ... represents the name of the original
    image
    """
    for fp in sorted(input_path.glob('**/*.jpg')):
        # print(f'Reading {fp}')
        left_image, right_image = split_image(fp)
    
        right_name = fp.name[:-4]+ '-01' #recall that last 4 are .jpg
        right_fp = (output_path / right_name ).with_suffix('.jpg')    
        
        left_name = fp.name[:-4]+ '-02' #recall that last 4 are .jpg
        left_fp = (output_path / left_name ).with_suffix('.jpg')
    
        right_image.save(right_fp)
        left_image.save(left_fp)
    print('Done!')

def extract_text(images_path, output_path):
    for fp in sorted(images_path.glob('**/*.jpg')):
        # print(f'Reading {fp}')
        text = pytesseract.image_to_string(Image.open(fp), lang='jpn_vert')
        new_fp = (output_path / fp.name).with_suffix('.txt')
        # print(f'Writing {new_fp}')
        with open(new_fp, 'w') as fout:
            fout.write(text)
    print('Done!')