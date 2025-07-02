import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import AuthAPI
from routes.debug import DebugAPI
from fastapi.staticfiles import StaticFiles
import config

class App:
    def __init__(self):
        self.app = FastAPI()
        self.setup_middleware()
        self.app.mount("/", StaticFiles(directory="public", html=True), name="public")
        self.app.include_router(AuthAPI().router)
        self.app.include_router(DebugAPI().router)

    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=config.ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app(self):
        return self.app

if __name__ == "__main__":
    uvicorn.run(App().get_app(), host=config.SERVICE_HOST, port=config.SERVICE_PORT)