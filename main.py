import uvicorn
from fastapi import FastAPI
from routers import auth
from routers import transactions
from routers import wallets


app = FastAPI(
    title="CashPe API",
    description="CashPe swagger documentation",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)


app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(wallets.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        access_log=True,
        reload=True
    )