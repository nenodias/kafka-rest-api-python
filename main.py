import os
import subprocess
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from app.infraestructure.web import post_on_topic
from app.infraestructure.criptografia import build_ca_pems, build_rsa_pems

class GenerateCert(BaseModel):
    certname: str
    password: str

app = FastAPI(title="KafkaRest API",
    description="KafkaRest",
    version="1.0.0",
    docs_url="/swagger-ui.html",
    swagger_ui_parameters={"syntaxHighlight": True}
)


post_on_topic = app.post("/topic")(post_on_topic)

def generate_pem(keystore_p12: str, password: str):
    prefix = os.getcwd() + os.sep + "uploads" + os.sep
    password_bytes = password.encode()
    
    
    build_ca_pems(prefix + keystore_p12, password_bytes)
    build_rsa_pems(prefix + keystore_p12, password_bytes)
    

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    os.makedirs('uploads', exist_ok=True)
    with open("uploads/"+ file.filename, "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

@app.post("/generate-cert")
async def generate_cert(dto: GenerateCert):
    generate_pem(dto.certname, dto.password)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

