import sys
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

# Load the BLIP-VQA model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

def generate_answer(image: Image.Image, question: str) -> str:
    # Load the BLIP-VQA model and processor
    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

    
    """
    Generate an answer to a question about the given image.
    """
    inputs = processor(image, question, return_tensors="pt")
    outputs = model.generate(**inputs)
    answer = processor.decode(outputs[0], skip_special_tokens=True)
    return answer

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python script.py <image_path> <question>")
        sys.exit(1)

    image_path = sys.argv[1]
    question = " ".join(sys.argv[2:])

    try:
        image = Image.open(image_path)
        answer = generate_answer(image, question)
        print("Answer:", answer)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
