from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError

from src.core.config import settings
from src.api.router import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API de gestión de tareas con autenticación JWT",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{settings.PROJECT_NAME}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #DBDEED 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                background: white;
                padding: 3rem;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 500px;
            }}
            .logo {{
                font-size: 4rem;
                margin-bottom: 1rem;
            }}
            h1 {{
                color: #333;
                margin-bottom: 0.5rem;
                font-size: 2.5rem;
            }}
            .version {{
                color: #888;
                font-size: 0.9rem;
                margin-bottom: 2rem;
            }}
            .description {{
                color: #666;
                margin-bottom: 2rem;
                line-height: 1.6;
            }}
            .links {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .btn {{
                padding: 0.8rem 1.5rem;
                border-radius: 10px;
                text-decoration: none;
                font-weight: 600;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
            }}
            .btn-primary {{
                background: linear-gradient(135deg, #667eea 100%);
                color: white;
            }}
            .btn-secondary {{
                background: #f0f0f0;
                color: #333;
            }}
            .status {{
                margin-top: 2rem;
                padding: 0.5rem 1rem;
                background: #d4edda;
                color: #155724;
                border-radius: 20px;
                font-size: 0.85rem;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">📋</div>
            <h1>{settings.PROJECT_NAME}</h1>
            <p class="version">v{settings.PROJECT_VERSION}</p>
            <p class="description">
                API de gestión de tareas con autenticación JWT, 
                roles y permisos personalizables.
            </p>
            <div class="links">
                <a href="/docs" class="btn btn-primary">📖 Swagger UI</a>
                <a href="/redoc" class="btn btn-secondary">📚 ReDoc</a>
            </div>
            <div class="status">✅ API funcionando correctamente</div>
        </div>
    </body>
    </html>
    """


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor"},
    )


app.include_router(api_router)