from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader
from fastapi.middleware.cors import CORSMiddleware

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):

    loader = YoutubeLoader.from_youtube_url(str(request.youtube_link), add_video_info=True)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    result = text_splitter.split_documents(docs)

    print(f"{type(result)}")
    author = result[0].metadata['author']
    length = result[0].metadata['length']
    title = result[0].metadata['title']
    total_size = len(result)

    return{
        "author": author,
        "length": length,
        "title": title,
        "total_size": total_size,
    }

