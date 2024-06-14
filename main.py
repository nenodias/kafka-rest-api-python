from fastapi import FastAPI
from app.infraestructure.web import post_on_topic

app = FastAPI(title="KafkaRest API",
    description="KafkaRest",
    version="1.0.0",
    docs_url="/swagger-ui.html",
    swagger_ui_parameters={"syntaxHighlight": True}
)


post_on_topic = app.post("/topic")(post_on_topic)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

