from fastapi import Depends, Request, Body, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import routes.utils

class Frontend:
    def __init__(self):
        self.router = APIRouter(prefix="/app", tags=["App"])
        self.templates = Jinja2Templates(directory="templates")
        self.router.add_api_route("/", self.read_root, methods=["GET"])
        
    async def read_root(self, request: Request):
        # ambil cookie
        # validasi cookie
        # jika tidak ada tunjukan login
        # jika ada tunjukan dashboard seuai role

        user_ip = request.client.host
        access_token = request.cookies.get("access_token")
        aud = request.headers.get("user-agent")

        validator = await routes.utils.validate_token(access_token, user_ip, aud);
        print(validator)

        data = {"name": "Budi", "hobi": ["ngoding", "ngopi", "tidur"]}
        return self.templates.TemplateResponse("index.html", {"request": request, **data})