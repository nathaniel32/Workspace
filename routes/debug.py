from fastapi import Depends, Request, Body, APIRouter
import database.connection
import database.models
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
    
    def debug_add_data(self, db: database.connection.db_dependency):
        # TUser
        user1 = database.models.TUser(u_id='user1', u_name='Alice', u_email='alice@example.com', u_password='hashed_pw1', u_role=database.models.UserRole.USER)
        user2 = database.models.TUser(u_id='user2', u_name='Nathaniel', u_email='nathaniel@example.com', u_password='hashed_pw2', u_role=database.models.UserRole.ADMIN)

        # TPower
        power1 = database.models.TPower(p_id='power1', p_power=100)
        power2 = database.models.TPower(p_id='power2', p_power=200)
        power3 = database.models.TPower(p_id='power3', p_power=300)
        power4 = database.models.TPower(p_id='power4', p_power=400)
        power5 = database.models.TPower(p_id='power5', p_power=500)
        power6 = database.models.TPower(p_id='power6', p_power=1000)

        # TSpec
        spec1 = database.models.TSpec(s_id='spec1', s_spec='Preventive Price List')
        spec2 = database.models.TSpec(s_id='spec2', s_spec='Change bearing unit')
        spec3 = database.models.TSpec(s_id='spec3', s_spec='Change Volute Casing')

        # TPriceList
        """ pricelists = [
            database.models.TPriceList(p_id='power1', s_id='spec1', pl_price=Decimal('590000.00')),
            database.models.TPriceList(p_id='power1', s_id='spec2', pl_price=Decimal('500100.00')),
            database.models.TPriceList(p_id='power1', s_id='spec3', pl_price=Decimal('550000.00')),

            database.models.TPriceList(p_id='power2', s_id='spec1', pl_price=Decimal('1500000.00')),
            database.models.TPriceList(p_id='power2', s_id='spec2', pl_price=Decimal('2500000.00')),
            database.models.TPriceList(p_id='power2', s_id='spec3', pl_price=Decimal('555000.00')),

            database.models.TPriceList(p_id='power3', s_id='spec1', pl_price=Decimal('160000.00')),
            database.models.TPriceList(p_id='power3', s_id='spec2', pl_price=Decimal('201000.00')),
            database.models.TPriceList(p_id='power3', s_id='spec3', pl_price=Decimal('101000.00')),

            database.models.TPriceList(p_id='power4', s_id='spec1', pl_price=Decimal('1500000.00')),
            database.models.TPriceList(p_id='power4', s_id='spec2', pl_price=Decimal('1540000.00')),
            database.models.TPriceList(p_id='power4', s_id='spec3', pl_price=Decimal('550000.00')),

            database.models.TPriceList(p_id='power5', s_id='spec1', pl_price=Decimal('1500000.00')),
            database.models.TPriceList(p_id='power5', s_id='spec2', pl_price=Decimal('505000.00')),
            database.models.TPriceList(p_id='power5', s_id='spec3', pl_price=Decimal('1100000.00')),

            database.models.TPriceList(p_id='power6', s_id='spec1', pl_price=Decimal('1505000.00')),
            database.models.TPriceList(p_id='power6', s_id='spec2', pl_price=Decimal('1510000.00')),
            database.models.TPriceList(p_id='power6', s_id='spec3', pl_price=Decimal('1210000.00')),
        ] """

        # TOrder
        order1 = database.models.TOrder(o_id='order1', u_id='user1', o_description='untuk PT. OPT')
        order2 = database.models.TOrder(o_id='order2', u_id='user2', o_description='untuk PT. DFG')
        order3 = database.models.TOrder(o_id='order3', u_id='user2', o_description='untuk PT. DFG')

        # TOrderArticle
        order_articles = [
            database.models.TOrderArticle(oa_id='oa1', p_id='power1', o_id='order1', opl_description='FP-01-PM-P1'),
            database.models.TOrderArticle(oa_id='oa2', p_id='power2', o_id='order2', opl_description='FP-01-SP-P2'),
            database.models.TOrderArticle(oa_id='oa3', p_id='power3', o_id='order2', opl_description='FP-01-PM-P2'),
            database.models.TOrderArticle(oa_id='oa4', p_id='power4', o_id='order3', opl_description='FP-01-PM-P2'),
            database.models.TOrderArticle(oa_id='oa5', p_id='power2', o_id='order3', opl_description='FP-01-PM-P2'),
        ]

        # TOrderSpec
        order_specs = [
            database.models.TOrderSpec(oa_id='oa1', p_id='power1', s_id='spec1', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa1', p_id='power1', s_id='spec2', os_price=Decimal('100000.00')),

            database.models.TOrderSpec(oa_id='oa2', p_id='power2', s_id='spec1', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa2', p_id='power2', s_id='spec2', os_price=Decimal('100000.00')),

            database.models.TOrderSpec(oa_id='oa3', p_id='power3', s_id='spec1', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa3', p_id='power3', s_id='spec2', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa3', p_id='power3', s_id='spec3', os_price=Decimal('100000.00')),

            database.models.TOrderSpec(oa_id='oa4', p_id='power4', s_id='spec2', os_price=Decimal('100000.00')),

            database.models.TOrderSpec(oa_id='oa5', p_id='power2', s_id='spec3', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa5', p_id='power2', s_id='spec2', os_price=Decimal('100000.00')),
            database.models.TOrderSpec(oa_id='oa5', p_id='power2', s_id='spec1', os_price=Decimal('100000.00')),
        ]

        try:
            db.add_all([
                user1, user2,
                power1, power2, power3, power4, power5, power6,
                spec1, spec2, spec3,
                order1, order2, order3,
                #*pricelists,
                *order_articles,
                *order_specs
            ])
            db.commit()
            return {"message": "Dummy data inserted successfully"}
        except Exception as e:
            db.rollback()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail="Beim Speichern der Dummy-Daten ist ein Fehler aufgetreten: " + str(e))