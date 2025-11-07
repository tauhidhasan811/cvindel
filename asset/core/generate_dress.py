import re
import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from langchain_core.messages import HumanMessage

def safe_base64_to_image(base64_str: str) -> Image.Image:
    if not base64_str or not isinstance(base64_str, str):
        raise ValueError("Empty or invalid input string.")

    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]

    # Remove whitespace / line breaks
    base64_str = base64_str.replace("\n", "").replace("\r", "").strip()

    # Keep only valid Base64 chars
    base64_str = re.sub(r"[^A-Za-z0-9+/=]", "", base64_str)

    # Fix padding
    missing_padding = len(base64_str) % 4
    if missing_padding:
        base64_str += "=" * (4 - missing_padding)

    # Quick check: minimum length of a valid image Base64
    if len(base64_str) < 100:
        raise ValueError("The Base64 string is too short, likely not an image.")

    try:
        image_bytes = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_bytes))
        return image
    except (base64.binascii.Error, UnidentifiedImageError) as e:
        raise ValueError(
            "Failed to decode image: The model probably returned text instead of a Base64 image."
        ) from e

def generate_image_from_dict(model, attributes: dict) -> Image.Image:
    prompt_text = "Generate a realistic image of a person with the following attributes:\n"
    for key, value in attributes.items():
        prompt_text += f"{key}: {value}\n"

    human = HumanMessage(
        content=[{"type": "text", "text": prompt_text}]
    )

    response = model.invoke([human])

    # Attempt to convert to image
    image = safe_base64_to_image(response.content)
    return image


'''
def generate_image_from_dict(model, attributes: dict) -> Image.Image:
    """
    Generates an image from a dictionary of attributes using a Gemini image model.

    Args:
        model: LangChain Gemini model instance (ChatGoogleGenerativeAI).
        attributes (dict): Dictionary with keys like 'skin_tone', 'age', 'gender', etc.

    Returns:
        PIL.Image.Image: Generated image.
    """

    # --- Step 1: Create prompt text ---
    prompt_text = "Generate a realistic image of a person with the following attributes:\n"
    for key, value in attributes.items():
        prompt_text += f"{key}: {value}\n"

    # --- Step 2: Wrap in HumanMessage ---
    human = HumanMessage(
        content=[{"type": "text", "text": prompt_text}]
    )

    # --- Step 3: Call the model ---
    response = model.invoke([human])

    # --- Step 4: Extract Base64 string ---
    base64_image_str = response.content.strip()
    
    # Remove data URI prefix if present
    if base64_image_str.startswith("data:image"):
        base64_image_str = base64_image_str.split(",")[1]

    # Remove any newlines or spaces
    base64_image_str = base64_image_str.replace("\n", "").replace("\r", "").strip()

    # Fix padding if missing
    missing_padding = len(base64_image_str) % 4
    if missing_padding:
        base64_image_str += "=" * (4 - missing_padding)

    # --- Step 5: Decode and open image ---
    image_bytes = base64.b64decode(base64_image_str)
    image = Image.open(BytesIO(image_bytes))

    return image
'''