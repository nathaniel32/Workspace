from fastapi import Depends, Request, Body, APIRouter
from fastapi.templating import Jinja2Templates
import routes.utils

class Frontend:
    def __init__(self):
        self.router = APIRouter(tags=["App"])
        self.templates = Jinja2Templates(directory="templates")
        self.router.add_api_route("/", self.root, methods=["GET"])
        self.router.add_api_route("/dashboard", self.dashboard, methods=["GET"])
        
    async def root(self, request: Request):
        url = "/dashboard"
        return routes.utils.return_site(request=request, templates=self.templates, url=url, redirect=True)

    async def dashboard(self, request: Request):
        url = "dashboard.html"
        return routes.utils.return_site(request=request, templates=self.templates, url=url)