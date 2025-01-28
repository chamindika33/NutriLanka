from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from bin.routers.food_router import router

import uvicorn




app = FastAPI(
    title="Halo Connect - Merchant Manager",
    contact={
        "name": "chamindika Kodithuwakku",
        "email": "chamindika1996@gmail.com",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002, workers=1, reload=False)

    
    

    

     