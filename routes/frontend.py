from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
import routes.api.utils
from fastapi.responses import RedirectResponse

class Frontend:
    def __init__(self):
        self.router = APIRouter(tags=["App"])
        self.templates = Jinja2Templates(directory="public/templates")
        self.router.add_api_route("/", self.root, methods=["GET"])
        self.router.add_api_route("/dashboard", self.dashboard, methods=["GET"])
        
    async def root(self, request: Request):
        payload, context= routes.api.utils.auth_site(request=request)

        if payload and payload.get("role"):
            url = "/dashboard"
            return RedirectResponse(url=url)
        
        url="shared/base.html"
        return self.templates.TemplateResponse(url, context, status_code=401)

    async def dashboard(self, request: Request):
        payload, context= routes.api.utils.auth_site(request=request)
        
        if payload and payload.get("role"):
            url = "dashboard.html"
            return self.templates.TemplateResponse(url, context)
        
        url = "/"
        return RedirectResponse(url=url)