from fastapi import FastAPI, Response
import subprocess
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "IAPIAUIENSE online e funcionando!"}

@app.post("/processar")
def processar(url: str):
    output_file = "output.mp4"
    if os.path.exists(output_file):
        os.remove(output_file)
    
    comando_download = f"yt-dlp -f best -o video_original.mp4 {url}"
    subprocess.run(comando_download, shell=True)
    
    comando_corte = "ffmpeg -i video_original.mp4 -vf \"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920\" -c:a copy output.mp4"
    subprocess.run(comando_corte, shell=True)
    
    return {"mensagem": "Processado com sucesso!"}

@app.get("/video")
def baixar_video():
    output_file = "output.mp4"
    if os.path.exists(output_file):
        with open(output_file, "rb") as f:
            video_bytes = f.read()
        return Response(content=video_bytes, media_type="video/mp4")
    return {"erro": "Nenhum vídeo processado ainda."}
