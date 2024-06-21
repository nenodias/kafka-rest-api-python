import os
import subprocess
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from app.infraestructure.web import post_on_topic

class GenerateCert(BaseModel):
    certname: str

app = FastAPI(title="KafkaRest API",
    description="KafkaRest",
    version="1.0.0",
    docs_url="/swagger-ui.html",
    swagger_ui_parameters={"syntaxHighlight": True}
)


post_on_topic = app.post("/topic")(post_on_topic)

def generate_pem(keystore_p12):
    output_suffix = keystore_p12.replace("_keystore.p12", "")
    output_caroot = f"{output_suffix}_caroot.pem"
    output_rsakey = f"{output_suffix}_rsakey.pem"
    print(f"openssl pkcs12 -in uploads/{keystore_p12} -out uploads/{output_caroot}")
    subprocess.call(f"openssl pkcs12 -in uploads/{keystore_p12} -out uploads/{output_caroot}", shell=True, stderr=subprocess.STDOUT, executable="/bin/bash")
    print(f"openssl pkcs12 -in uploads/{keystore_p12} -nodes -nocerts -out uploads/{output_rsakey}")
    subprocess.call(f"openssl pkcs12 -in uploads/{keystore_p12} -nodes -nocerts -out uploads/{output_rsakey}", shell=True, stderr=subprocess.STDOUT, executable="/bin/bash")
    # Move
    subprocess.call(f"mv uploads/{output_caroot} certs/{output_caroot}", shell=True, stderr=subprocess.STDOUT, executable="/bin/bash")
    subprocess.call(f"mv uploads/{output_rsakey} certs/{output_rsakey}", shell=True, stderr=subprocess.STDOUT, executable="/bin/bash")
    

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    os.mkdir('uploads')
    with open("uploads/"+ file.filename, "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

@app.post("/generate-cert")
async def generate_cert(dto: GenerateCert):
    generate_pem(dto.certname)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

