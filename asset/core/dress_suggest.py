import json
from dotenv import load_dotenv
#from asset.core.wardrobe_suggest import users_wardrobe
from asset.database_manage.dressRepo import get_by_userid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def suggester(human_info,dress_info, model):

    
    full_data = {
        "user_information": human_info,
        "dresses_information": dress_info
    }

    # System instruction
    system = SystemMessage(
        content=(
            "You are a professional fashion designer and stylist. This is mostly for young people from 20-40 years old. Try to be bold and cool such that it matches the vibe of the user."
            "Analyze the given user information along with their plans and weather reports, then generate an outfit suggestion. Ensure the suggestion is trendy and upto date of the user's region and weather."
            "Provide one/more valid shopping websites/urls for the suggested outfits that are available on the web. Make sure that the website is active in user's country without any overseas shippping."
            "All items that are worn above waist or onepiece or female swimsuits is categorized as tops. Return strictly in the JSON format provided, without any extra text, explanation, or quotes. "
        )
    )

    # Example output template
    output_template = {
        "outfit": [
            {
                "category": "tops",
                "attributes": {
                    "type": "Shirt",
                    "color": "Grey",
                    "pattern": "Solid",
                    "material": "Cotton",
                    "fit": "Slim fit",
                    "season": "Summer",
                    "preference": "Classy",
                    "style": "Formal",
                    "image": ["Provide one/more valid shopping websites/urls for the suggested outfits that are available on the web."],
                    "features": ["Buttoned front", "Short sleeves"],
                    "sleeve_type": "Short sleeve",
                    "neck_type": "Collar"
                }
            },
            {
                "category": "bottoms",
                "attributes": {
                    "type": "Trousers",
                    "color": "Navy",
                    "pattern": "Solid",
                    "material": "Linen",
                    "fit": "Slim fit",
                    "season": "Summer",
                    "preference": "Classy",
                    "style": "Formal",
                    "image": ["Provide one/more valid shopping websites/urls for the suggested outfits that are available on the web."],
                    "features": ["Pockets"],
                    "length": "Full length",
                    "waist_type": "Mid waist"
                }
            },
            {
                "category": "shoes",
                "attributes": {
                    "type": "Loafers",
                    "color": "Brown",
                    "pattern": "Solid",
                    "material": "Leather",
                    "fit": "Regular",
                    "season": "All-season",
                    "preference": "Formal",
                    "style": "Office",
                    "image": ["Provide one/more valid shopping websites/urls for the suggested outfits that are available on the web."],
                    "closure": "Slip-on",
                    "heel_height": "Low",
                    "sole_type": "Rubber",
                    "features": ["Non-slip", "Comfortable insole"]
                }
            }
        ],
        "full_instruction": "Suggest the outfit with full detailed instruction to wear them that was generated in the outfut portion",
        'dessid': 'give just id from the all_dresses data if matched with the suggested if not matched no needed as this fo;;owing sructure {"top": match top parts id , "bottom" : bottom parts id, "shoes" : shoes id}',
        "urls": ["add all the image urls of the outfits that was generated in the outfits section"]
    }

    # Human message
    human = HumanMessage(
        content=(
            f"Analyze this data: {full_data}. "
            f"Return your best estimate strictly in this JSON format: {output_template}. "
            "Do NOT include any extra text, quotes, or commentary."
        )
    )

    # Invoke the model
    response = model.invoke([system, human])
    print(f"\n\nResponse message: {response} \n\n")
    result = response.content.strip()

    # Strip code fences safely if present
    if result.startswith("```") and result.endswith("```"):
        result_lines = result.splitlines()

        result = "\n".join(result_lines[1:-1])

    try:
        result_json = json.loads(result)
        if human_info['_id']:
            print(f'User ID found. ID is {human_info["_id"]}')
            #wardrobe = users_wardrobe(human_info['_id'], result_json["outfit"])

    except json.JSONDecodeError:
        print("⚠️ Model did not return valid JSON. Raw output:")
        print(response.content)
        result_json = {"error": "Invalid JSON response"}

    return result_json
