from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://your-production-frontend.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
