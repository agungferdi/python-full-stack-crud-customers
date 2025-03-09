from flask import Blueprint
from .customer_routes import register_customer_routes
from .address_routes import register_address_routes


api_blueprint = Blueprint('api', __name__)


register_customer_routes(api_blueprint)
register_address_routes(api_blueprint)

__all__ = ['api_blueprint']