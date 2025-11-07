
import json
import ast
from asset.core.weather import get_temp
from asset.core.dress_suggest import suggester
from asset.helper.commonfecture import model_name
from langchain_google_genai import ChatGoogleGenerativeAI
from asset.database_manage.dressRepo import get_by_userid
from asset.database_manage.userRepo import get_userinfo



def FullSuggestion(lat, lon, additional_data, user_id=0):
    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
    geographical_data = get_temp(lat, lon)
    if user_id is not None:
        facial_data= get_userinfo(user_id)
        dresses = get_by_userid(userid=user_id)
        print(f'type of facial data is {type(facial_data)}\nThe facial data is {facial_data}')
    else:
        return "Please Enter userid"
    
    merge = {**facial_data, **additional_data, **geographical_data}
    
    res = suggester(human_info=merge,dress_info=dresses, model=model)

    dressid, urls, text = None, None, {}
    print('dress suggestion is returned succesfully from the suggester')
    if isinstance(res, str):
        clean_text = (
            res.replace("```json", "")
               .replace("```", "")
               .strip()
        )

        print('debugger 1')
        try:
            parsed = json.loads(clean_text)
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(clean_text)
            except Exception:
                print("Model output is not valid JSON or Python dict. Returning raw text.")
                return None, None, merge, {"error": "Invalid JSON response"}
        dressid = parsed.get("dressid") or parsed.get("dessid")
        urls = parsed.get("urls")
        parsed.pop("dressid", None)
        parsed.pop("dessid", None)
        parsed.pop("urls", None)

        text = parsed

    elif isinstance(res, dict):
        print('debuger 2')
        dressid = res.get("dressid") or res.get("dessid")
        urls = res.get("urls")
        text = {k: v for k, v in res.items() if k not in ["dressid", "dessid", "urls"]}
        print('debugger 2 is completed successfully')

    else:
        print("Unexpected result format from suggester()")
        text = {"error": "Unexpected output format"}


    return dressid, urls, merge, text
