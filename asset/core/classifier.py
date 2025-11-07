import ast
import base64
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def classifier(img_type, image_path, model):
    
    if img_type == 'human':
        system = SystemMessage(
            content=(
                "You are a personal assistant that analyzes human appearance from images. "
                "Respond concisely using only the specified output format."
            )
        )
        output_ins = {
            "skin_tone": "color_name",
            "race":"White/Caucasian/European/Asian/Indain/SouthEasteern/etc.",
            "age": "number",
            "gender": "male/female",
            "fitness": "fit/healty/athletic/chubby/plus sized"
        }
    elif img_type == 'dress':
        system = SystemMessage(
            content=(
                "You are a professional fashion stylist and clothing analyst. "
                "You will analyze an image and identify each clothing item in it. "
                "Each clothing item must be categorized as either a 'top', 'bottom', or 'shoes'.\n\n"
                "For each detected clothing item, return a dictionary with its attributes. "
                "If multiple items are present, return a list of such dictionaries.\n\n"
                "Each item has the following common attributes:\n"
                "  - type: the specific item name (e.g., shirt, pants, sneakers)\n"
                "  - color: main color\n"
                "  - pattern: Solid, Striped, Checked, Floral, etc.\n"
                "  - material: Cotton, Denim, Leather, etc.\n"
                "  - fit: Slim fit, Loose, Regular, etc.\n"
                "  - season: Summer, Winter, etc.\n"
                "  - preference: Classy, Sporty, Minimalist, etc.\n"
                "  - style: Casual, Formal, Streetwear, etc.\n"
                "  - image: URL of the cropped clothing item (if available)\n"
                "  - features: unique notable details (e.g., Pockets, Buttons, Laces, Waterproof)\n\n"
                "Then, depending on the category, include the unique attributes:\n"
                "  - For TOP: sleeve_type, neck_type\n"
                "  - For BOTTOM: length, waist_type\n"
                "  - For SHOES: closure, heel_height, sole_type\n\n"
                "The final output must always be a list of JSON objects like this:\n"
                "[\n"
                "  {\n"
                "    'category': 'top',\n"
                "    'type': 'Shirt',\n"
                "    'color': 'Grey',\n"
                "    'pattern': 'Solid',\n"
                "    'material': 'Cotton',\n"
                "    'fit': 'Slim fit',\n"
                "    'season': 'Summer',\n"
                "    'preference': 'Classy',\n"
                "    'style': 'Formal',\n"
                "    'image': 'https://example.com/item1.jpg',\n"
                "    'features': ['Buttons'],\n"
                "    'sleeve_type': 'Short sleeve',\n"
                "    'neck_type': 'Collar'\n"
                "  }\n"
                "]"
            )
        )
        output_ins = {
            "category": "top/neckwear/bottom/shoes",
            "type": "specific item name (shirt, jeans, sneakers, etc.)",
            "color": "main_color",
            "pattern": "pattern_style",
            "material": "material_type",
            "fit": "fit_type",
            "season": "season_type",
            "preference": "Classic/Minimalist/Sporty/Edgy/Boho/Streetwear",
            "style": "style_type",
            "image": "image_url",
            "features": ["list_of_features"],
            "unique_fields": {
                "top": ["sleeve_type", "neck_type"],
                "bottom": ["length", "waist_type"],
                "shoes": ["closure", "heel_height", "sole_type"]
            }
        }

    else:
        raise ValueError("Invalid img_type. Must be 'human' or 'dress'.")

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    human = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    f"Analyze this image and return your best estimate in this exact format "
                    f"without any extra words, commas, or quotes: {output_ins}"
                )
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            }
        ]
    )

    response = model.invoke([system, human])
    response.content
    result = ast.literal_eval(response.content)
    print(result)
    return result

