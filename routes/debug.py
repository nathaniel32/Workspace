from fastapi import Depends, Request, Body, APIRouter
import database
from decimal import Decimal

class DebugAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/debug", tags=["Debug"])
        self.router.add_api_route("/request", self.debug_request, methods=["GET"])
        self.router.add_api_route("/add_data", self.debug_add_data, methods=["POST"])

    async def debug_request(self, request: Request):
        headers = dict(request.headers)
        cookies = request.cookies
        query_params = dict(request.query_params)
        client_host = request.client.host if request.client else "Unknown"
        method = request.method
        url = str(request.url)
        body = await request.body()
        
        return {
            "method": method,
            "url": url,
            "client_ip": client_host,
            "headers": headers,
            "cookies": cookies,
            "query_params": query_params,
            "body": body.decode("utf-8") if body else None
        }
    
    def debug_add_data(self, db: database.db_dependency):

        # Dummy data buat TUser
        user1 = database.TUser(u_id='user1', u_name='Alice', u_email='alice@example.com', u_password='hashed_pw1', u_role=database.UserRole.USER)
        user2 = database.TUser(u_id='user2', u_name='Bob', u_email='bob@example.com', u_password='hashed_pw2', u_role=database.UserRole.ADMIN)

        # Dummy data buat TPower
        power1 = database.TPower(p_id='power1', p_kw=100)
        power2 = database.TPower(p_id='power2', p_kw=200)

        # Dummy data buat TSpec
        spec1 = database.TSpec(s_id='spec1', s_kw='SpecA')
        spec2 = database.TSpec(s_id='spec2', s_kw='SpecB')

        # Dummy data buat TArticle
        article1 = database.TArticle(p_id='power1', s_id='spec1', a_name='Article 1', a_description='Description 1', a_price=Decimal('50.00'))
        article2 = database.TArticle(p_id='power2', s_id='spec2', a_name='Article 2', a_description='Description 2', a_price=Decimal('150.00'))

        # Dummy data buat TOrder
        order1 = database.TOrder(o_id='order1', u_id='user1', o_description='Order for Alice')
        order2 = database.TOrder(o_id='order2', u_id='user2', o_description='Order for Bob')

        # Dummy data buat TOrderArticle (composite PK oa_id + p_id)
        order_article1 = database.TOrderArticle(oa_id='oa1', p_id='power1', o_id='order1', oa_description='OrderArticle 1 desc')
        order_article2 = database.TOrderArticle(oa_id='oa2', p_id='power2', o_id='order2', oa_description='OrderArticle 2 desc')

        # Dummy data buat TOrderSpec
        order_spec1 = database.TOrderSpec(os_id='os1', oa_id='oa1', p_id='power1', s_id='spec1', os_price=Decimal('55.00'))
        order_spec2 = database.TOrderSpec(os_id='os2', oa_id='oa2', p_id='power2', s_id='spec2', os_price=Decimal('160.00'))

        try:
            db.add_all([
                user1, user2, power1, power2, spec1, spec2,
                article1, article2, order1, order2,
                order_article1, order_article2, order_spec1, order_spec2
            ])
            db.commit()
            return {"message": "Dummy data inserted successfully"}
        except Exception as e:
            db.rollback()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail="Beim Speichern der Benutzerdaten ist ein Fehler aufgetreten: " + str(e))