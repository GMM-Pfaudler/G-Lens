from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth,ofn_router,ga_router,test_router
from app.routers import ofn_ga_comparison,ga_ga_comparison,full_bom_router,model_vs_bom_comparison,image_comparison_router,sse_router,activity_log_router
import uvicorn

app = FastAPI()

# -----------------------------
# CORS setup
# -----------------------------

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    # "https://glens.gmmpfualder.com",
    # "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message":"Backend Running successfully."}

# include auth endpoints
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# include OFN endpoints
app.include_router(ofn_router.router, prefix="/api/ofn", tags=["OFN"])

#include GA endpoints
app.include_router(ga_router.router, prefix="/api/ga", tags=["GA"])

# # include Test endpoint
# app.include_router(test_router.router, prefix="/api/test")

app.include_router(ofn_ga_comparison.router, prefix="/api/comparison/ofn-ga", tags=["OFN-to-GA Comparison"])

app.include_router(ga_ga_comparison.router, prefix="/api/comparison/ga-ga",tags=["GA-to-GA Comparison"])

app.include_router(full_bom_router.router, prefix="/api/comparison", tags=["Full BOM Comparison"])

app.include_router(model_vs_bom_comparison.router, prefix="/api/comparison", tags=["Model vs BOM Comparison"])

app.include_router(image_comparison_router.router,prefix="/api/comparison", tags=["File/Image Comparison"])

app.include_router(activity_log_router.router)

# SSE Router
app.include_router(sse_router.router, prefix="/api/sse", tags=["SSE"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)