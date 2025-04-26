import sys
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the BLIP model and processor once at the start of your program
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_description(image: Image.Image) -> str:
    """
    This method takes a PIL image, processes it, and returns a generated description.

    Args:
        image (PIL.Image): A PIL image object.

    Returns:
        str: The generated description of the image.
    """
    # Process the image
    inputs = processor(images=image, return_tensors="pt")

    # Generate a caption
    out = model.generate(**inputs)

    # Decode the generated caption
    caption = processor.decode(out[0], skip_special_tokens=True)

    return caption

def main():
    """
    Main function that accepts an image path as a command line argument,
    loads the image, and generates a description.
    """
    # Check if the user provided an image file path as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)

    # Get the image path from the command line argument
    image_path = sys.argv[1]

    try:
        # Open the image using PIL
        image = Image.open(image_path)

        # Generate a description for the image
        description = generate_description(image)

        # Output the generated description
        print("Generated Description: ", description)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Entry point for the script
if __name__ == "__main__":
    main()
