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
        try:
            # redirect ke dashboard jika sudah login
            context = routes.api.utils.auth_site(request=request)
            url = "/dashboard"
            return RedirectResponse(url=url)
        except routes.api.utils.AuthException as e:
            url="shared/base.html"
            return self.templates.TemplateResponse(url, context=e.context) # status_code=401
        
    async def dashboard(self, request: Request):
        try:
            context= routes.api.utils.auth_site(request=request)
            url = "dashboard.html"
            return self.templates.TemplateResponse(url, context)
        except Exception:
            # redirect ke root jika belum login
            url = "/"
            return RedirectResponse(url=url)