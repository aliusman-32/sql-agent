from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlAgent import SQLAgent

app = FastAPI(title="SQL Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query : str

sql_agent = SQLAgent()
from fastapi.responses import JSONResponse

@app.post("/query")
async def execute_query(request: QueryRequest):
    try:
        response = sql_agent.response(request.query)
        print(response)
        
        return JSONResponse(content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Run FastAPI App ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    