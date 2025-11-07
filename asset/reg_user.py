from asset.core.classifier import classifier
from asset.core.register_user import register
from asset.helper.commonfecture import model_name
from langchain_google_genai import ChatGoogleGenerativeAI



def FacialData(img_path):

    additional_data = {'image': img_path}
    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
    facial_data = classifier(image_path=img_path, img_type='human', model=model)
    merge = {**facial_data, **additional_data}
    res = register(user_info=merge)

    return merge
