import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api.services.account import AccountAPI
from routes.api.services.element import ElementAPI
from routes.api.services.order import OrderAPI
from routes.api.services.sql_workbench import SQLWorkbenchAPI
from routes.frontend import Frontend
from routes.api.services.media import MediaAPI
from utils import config
from fastapi.staticfiles import StaticFiles
import services.exel_manager
import services.pdf_manager

class App:
    def __init__(self):
        self.app = FastAPI()
        self.setup_middleware()
        self.element_api = ElementAPI()
        self.excel_order_manager = services.exel_manager.ExcelManager()
        self.pdf_order_manager = services.pdf_manager.PDFManager()
        self.app.mount("/static", StaticFiles(directory="public/static"), name="static")
        self.app.include_router(Frontend().router)
        self.app.include_router(AccountAPI().router)
        self.app.include_router(self.element_api.router)
        self.app.include_router(MediaAPI(excel_order_manager=self.excel_order_manager, pdf_order_manager=self.pdf_order_manager, element_api = self.element_api).router)
        self.app.include_router(OrderAPI(excel_order_manager=self.excel_order_manager, pdf_order_manager=self.pdf_order_manager).router)
        self.app.include_router(SQLWorkbenchAPI().router)

    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=config.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app(self):
        return self.app

if __name__ == "__main__":
    uvicorn.run(App().get_app(), host=config.SERVICE_HOST, port=int(config.SERVICE_PORT))