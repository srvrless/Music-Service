"""File with settings and configs for the project"""

import os

from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'a8906ba1367b4fe455c9804207d4268cef42b1c9026ff8c6805802bc009036ea'


BASEDIR = os.getcwd()
LOGDIR = "logs"
LOGFILE = "moviestar.log"
BIND = "0.0.0.0"

#
# if len(sys.argv) < 2:
#     print("no env provided from Pipfile")
#     sys.exit(1)
#
# dotenv_path = join(dirname(__file__), f".env.{sys.argv[1]}")
# load_dotenv(dotenv_path)
#
# PORT = os.environ.get("PORT")
# WORKERS = os.environ.get("WORKERS")
# RELOAD = os.environ.get("RELOAD")
ORIGINS = "*"
# NB_ENV = os.environ.get("NB_ENV")

# def custom_openapi(  # noqa: C901, WPS210, WPS231
#         app: FastAPI,
#         response_schema: Optional[Dict[str, Any]] = None,
# ) -> Callable[[], Dict[str, Any]]:
#     """
#     Generate custom openAPI schema.
#
#     This function generates openapi schema based on
#     routes from FastAPI application.
#
#     :param app: current FastAPI application.
#     :param response_schema: json schema of the response.
#     :returns: actual schema generator.
#     """
#
#     def openapi_generator() -> Dict[str, Any]:  # noqa: WPS210, WPS231, WPS430
#         # If api schema already exists we do nothing.
#         if app.openapi_schema:
#             return app.openapi_schema
#
#         # Generate base API schema based on
#         # current application properties.
#         openapi_schema = get_openapi(
#             title=app.title,
#             version=app.version,
#             description=app.description,
#             routes=app.routes,
#             license_info=app.license_info,
#             contact=app.contact,
#             terms_of_service=app.terms_of_service,
#             tags=app.openapi_tags,
#             servers=app.servers,
#             openapi_version=app.openapi_version,
#         )
#
#         # Header type from configuration.
#         header_type = AuthJWT._header_type  # noqa: WPS437
#         scheme_name = f"{header_type} auth"
#
#         if "components" not in openapi_schema:
#             openapi_schema["components"] = {}
#
#         # Add security scheme configuration
#         # only if if jwt must be in headers.
#         # Because cokies schema doesn't work on
#         # swagger page.
#         if "headers" in AuthJWT._token_location:  # noqa: WPS437
#             openapi_schema["components"]["securitySchemes"] = {
#                 scheme_name: {
#                     "type": "apiKey",
#                     "in": "header",
#                     "name": AuthJWT._header_name,  # noqa: WPS437
#                     "description": (
#                         f"Enter: **'{header_type} &lt;JWT&gt;'**, "
#                         "where JWT is the access token"
#                     ),
#                     "bearerFormat": header_type,
#                 },
#             }
#
#         # Get all routes where jwt_optional() or jwt_required
#         api_router = [route for route in app.routes if isinstance(route, APIRoute)]
#
#         for route in api_router:
#             # Getting python sources of a handler function.
#             sources = inspect.getsource(route.endpoint)
#             # Handler requires JWT auth if any of these words
#             # exist in handler's source code.
#             jwt_flags = ["jwt_required", "fresh_jwt_required", "jwt_optional"]
#             for method in route.methods:
#                 # If handler has jwt_flag inside its source code
#                 # we add security schema in swagger spec.
#                 if any([flag in sources for flag in jwt_flags]):
#                     method_info = openapi_schema["paths"][route.path][method.lower()]
#                     method_info["security"] = [
#                         {scheme_name: []},
#                     ]
#                     method_info["responses"][401] = {  # noqa: WPS432
#                         "description": "Authorization failed",
#                     }
#                     if response_schema is not None:
#                         method_info["responses"][401][  # noqa: WPS220, WPS432
#                             "content"
#                         ] = {
#                             "application/json": {"schema": response_schema},
#                         }
#
#         # Applying generated openapi schema to our app.
#         app.openapi_schema = openapi_schema
#         return app.openapi_schema
#
#     return openapi_generator
