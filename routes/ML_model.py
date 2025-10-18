from fastapi import APIRouter, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware # Import this


try:
    similarity = pickle.load(open('./notebook/similarity.pkl', 'rb'))
    final_df = pd.read_pickle('./notebook/final_df.pkl')
except FileNotFoundError:
    print("ERROR: 'similarity.pkl' or 'final_df.pkl' not found.")
    print("Please run the Jupyter Notebook first to create these files.")
    exit()

@router.get("/recommandation", response_class=HTMLResponse)
async def get_recommandation_page(request: Request):
    anime_names_list = final_df['Name'].tolist()
    return templates.TemplateResponse("recommandation.html", {
        "request": request,
        "anime_names": anime_names_list  
    })

@router.get("/anime-list")
async def get_anime_list():
    return {"names": final_df['Name'].tolist()}


@router.get("/recommend/{anime_name}")
async def get_recommendations(anime_name: str):
    try:
        matches = final_df[final_df['Name'].str.lower() == anime_name.lower()]
        
        if matches.empty:
            partial_matches = final_df[final_df['Name'].str.contains(anime_name, case=False)]
            if partial_matches.empty:
                raise HTTPException(status_code=404, detail="Anime not found")
            anime_index = partial_matches.index[0]
            actual_name = final_df.iloc[anime_index]['Name']
        else:
            anime_index = matches.index[0]
            actual_name = final_df.iloc[anime_index]['Name']

        distances = list(enumerate(similarity[anime_index]))
        sorted_distances = sorted(distances, reverse=True, key=lambda x: x[1])

        recommendations = []
        for i in sorted_distances[1:11]:
            name = final_df.iloc[i[0]]['Name']
            recommendations.append(name)
        
        return {
            "searched_anime": actual_name,
            "recommendations": recommendations
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
