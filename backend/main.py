import os
import sys
import uuid
import shutil
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asset.reg_user import FacialData
from asset.dress_manage import DressManager
from asset.fashion_helper import FullSuggestion
from asset.helper.commonfecture import model_name
from langchain_google_genai import ChatGoogleGenerativeAI
from asset.database_manage.dressRepo import get_all, get_by_dressid, get_by_userid


app = FastAPI(title="AI Dress API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = ChatGoogleGenerativeAI(model=model_name)

@app.post("/api/user_reg")
async def register(
    file: UploadFile =File(...)
    ):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = FacialData(img_path=file_path)
        os.remove(file_path)
        return JSONResponse(result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/analyze-dress")
async def analyze_dress(
        userid: int= Form(...), 
        file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        print(f'file path is : {file_path}')
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = DressManager(dress_path=file_path, model=model, user_id=userid)

        os.remove(file_path)

        return JSONResponse(content={"result": str(result)})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/dresses")
async def api_get_all_dresses():
    try:
        data = get_all()
        return JSONResponse(content={"dresses": data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/dresses/{dress_id}")
async def api_get_dress_by_id(dress_id: int):
    try:
        data = get_by_dressid(dress_id)
        if not data:
            return JSONResponse(content={"error": "Dress not found"}, status_code=404)
        return JSONResponse(content={"dress": data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/dresses/user/{userid}")
async def api_get_dresses_by_userid(userid: int):
    try:
        data = get_by_userid(userid)
        return JSONResponse(content={"dresses": data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/api/generate-recommendation", tags=["FullSuggestion"])
async def generate_recommendation(
    userid: int= Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    occasion: str = Form(...),
    preference: str = Form(...),
    fit: str = Form(...)
):
        
    additional_data = {"occasion": occasion, "preference": preference, "fit": fit}
        
    dressid, urls, facial_data, text = FullSuggestion(
            user_id=userid, lat=lat, lon=lon, additional_data=additional_data
        )

    return {
            "dressid": dressid,
            "urls": urls,
            "facial_data": facial_data,
            "recommendation_text": text
        }
    
