from fastapi import Depends, Request, Body, APIRouter
from fastapi.templating import Jinja2Templates
import routes.utils
from database.models import UserRole

class Frontend:
    def __init__(self):
        self.router = APIRouter(tags=["App"])
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

        try:
            message, payload = routes.utils.validate_token(access_token, user_ip, aud);
            
            print(message)

            if payload:
                role = payload.get('role')

                if role == UserRole.USER:
                    return self.templates.TemplateResponse("role/user.html", {"request": request, "payload": payload, "registered": True})
                if role == UserRole.ADMIN:
                    return self.templates.TemplateResponse("role/admin.html", {"request": request, "payload": payload, "registered": True})
                if role == UserRole.GUEST:
                    return self.templates.TemplateResponse("role/guest.html", {"request": request, "payload": payload, "registered": True})

            return self.templates.TemplateResponse("shared/base.html", {"request": request, "registered": False}, status_code=401)
        except Exception as e:
            print("Unexpected error:", e)
            return self.templates.TemplateResponse("shared/base.html", {"request": request, "registered": False}, status_code=500)