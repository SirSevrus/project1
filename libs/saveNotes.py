import logging
from PIL import Image
from tqdm import tqdm
import img2pdf
import os
import sys

# Suppress all warnings by redirecting stderr
sys.stderr = open(os.devnull, 'w')

# Configure logging to log to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('log', 'app.log')),
        logging.StreamHandler()
    ]
)

def remove_alpha_channel(image_path):
    """
    Removes the alpha channel from an image if it exists, replacing it with a white background.

    Args:
        image_path (str): The file path of the image.

    Returns:
        Image: The image without an alpha channel.
    """
    try:
        with Image.open(image_path) as img:
            # Check if the image has an alpha channel (transparency)
            if img.mode in ("RGBA", "LA"):
                # Create a new image with a white background
                background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                background.paste(img, img.split()[-1])  # Paste using the alpha channel as a mask
                logging.info(f"Removed alpha channel from {image_path}")
                return background
            else:
                return img
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")
        raise

def create_pdf(pdf_name, images):
    """
    Creates a PDF from a list of image paths.

    Args:
        pdf_name (str): The name of the output PDF file.
        images (list): A list of image file paths to include in the PDF.

    """
    processed_images = []
    
    # Use a single loop to process images and save them temporarily
    for image_path in tqdm(images, desc="Processing Images"):
        try:
            # Process image to remove alpha channel and save as a temporary file
            img = remove_alpha_channel(image_path)
            img_path = image_path.replace(".png", "_processed.png")
            img.save(img_path)
            processed_images.append(img_path)
        except Exception as e:
            logging.error(f"Failed to process {image_path}: {e}")

    try:
        # Convert the processed images to a PDF
        if os.path.isdir(os.path.join("data", "pdf")) == False:
            os.makedirs(os.path.join("data", "pdf"))
        with open(os.path.join("data", "pdf", pdf_name), "wb") as file:
            file.write(img2pdf.convert(processed_images))
            logging.info(f"PDF created successfully: {pdf_name}")
    except Exception as e:
        logging.error(f"An error occurred while creating PDF: {e}")
    finally:
        # Clean up temporary images
        for img_path in processed_images:
            try:
                os.remove(img_path)
                logging.info(f"Deleted temporary file: {img_path}")
            except Exception as e:
                logging.error(f"Failed to delete temporary file {img_path}: {e}")

def create(pdf_name, file_dir):
    """
    Finds all PNG images in the specified directory and converts them to a single PDF.

    Args:
        pdf_name (str): The name of the output PDF file.
        file_dir (str): The directory containing the images.

    """
    # Get a list of all PNG files in the directory
    new_files = [os.path.join(file_dir, i) for i in os.listdir(file_dir) if i.endswith('.png')]

    # Log the start of the PDF creation process
    logging.info("Starting PDF creation")
    
    # Create the PDF from the images
    create_pdf(pdf_name, new_files)
    
    # Log the completion of the PDF creation process
    logging.info("PDF creation process completed")

# To use this script:
# create("output.pdf", "C:\\path\\to\\image\\directory")
