
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# ----------import packages
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routes.v1.life_span import combined_lifespan
from app.routes.v1.roles import roles_router
from app.routes.v1.accounts import account_router
from app.routes.v1.account_groups import account_group_router
from app.routes.v1.files import file_router
from app.routes.v1.media import media_router
from app.routes.v1.branches import branches_router
from app.routes.v1.branch_account_groups import branch_account_group_router
from app.routes.v1.accesses import accesses_router
from app.routes.v1.permissions import permissions_router
from app.utils.utils import get_current_user_for_docs

# from app.utils.websocket_connections import manager


app = FastAPI(lifespan=combined_lifespan,swagger_ui_parameters = {"docExpansion":"none"},docs_url=None, redoc_url=None, openapi_url=None,)


app.title = settings.app_name
app.version = settings.version




app.include_router(permissions_router, prefix="/api/v1", tags=["Permissions"])
app.include_router(roles_router, prefix="/api/v1", tags=["Roles"])
app.include_router(accesses_router, prefix="/api/v1", tags=["Role accesses"])
app.include_router(account_router, prefix="/api/v1", tags=["Accounts"])
app.include_router(account_group_router, prefix="/api/v1", tags=["Account Groups"])
app.include_router(media_router, prefix="/api/v1", tags=["Media"])
app.include_router(file_router, prefix="/api/v1", tags=["Files"])
app.include_router(branches_router, prefix="/api/v1", tags=["Branches"])
app.include_router(branch_account_group_router, prefix="/api/v1", tags=["Branch Account Groups"])



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(current_user: str = Depends(get_current_user_for_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI",swagger_ui_parameters={"docExpansion": "none"},)


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(current_user: str = Depends(get_current_user_for_docs)):
    return get_openapi(title="Custom OpenAPI", version="1.0.0", routes=app.routes)



Base.metadata.create_all(bind=engine)

app.mount("/files", StaticFiles(directory="files"), name="files")



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.get("/", tags=["Home"])
async def message( request: Request,):
    print(request)
    try:
        data = await request.json()  # Parse JSON data


        if not data:  # If data is empty
            raise HTTPException(status_code=400, detail="Empty JSON body received")

        print(str(data))  # Print as string
        return {"success": True, "message": "Data received", "data": data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")


add_pagination(app)
