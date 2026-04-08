import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, intent TEXT, plan TEXT, completed TEXT, timestamps DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

class QueryRequest(BaseModel):
    intent: str

async def mock_agent_stream(intent: str):
    # Context Agent
    yield f"data: {json.dumps({'agent': 'Context Agent', 'type': 'thought', 'content': 'Reading user intent...', 'status': 'running'})}\n\n"
    await asyncio.sleep(1)
    yield f"data: {json.dumps({'agent': 'Context Agent', 'type': 'thought', 'content': f'Analyzing context for intent: \"{intent}\"', 'status': 'running'})}\n\n"
    await asyncio.sleep(1)
    yield f"data: {json.dumps({'agent': 'Context Agent', 'type': 'action', 'content': 'Fetched current tasks: 12 open | Deadlines: 3 today | Energy State: Evening (Low focus).', 'status': 'done'})}\n\n"
    await asyncio.sleep(0.5)

    # Planning Agent
    yield f"data: {json.dumps({'agent': 'Planning Agent', 'type': 'thought', 'content': 'Scoring tasks using priority matrix (Urgency × Importance × Duration × Energy)...', 'status': 'running'})}\n\n"
    await asyncio.sleep(2)
    plan_data = [
        {"task": "Prepare PPT for Hackathon", "score": 98, "duration": "45m"},
        {"task": "Deploy to Cloud Run", "score": 95, "duration": "30m"},
        {"task": "Record 3 min Demo", "score": 92, "duration": "45m"}
    ]
    if "lost 2 hours" in intent.lower():
        plan_data = [
             {"task": "Deploy to Cloud Run", "score": 99, "duration": "30m", "note": "Priority escalated. Danger of missing deadline."},
             {"task": "Record 3 min Demo", "score": 95, "duration": "30m", "note": "Adjusted duration.", "reduced": True}
        ]
        yield f"data: {json.dumps({'agent': 'Planning Agent', 'type': 'thought', 'content': 'Time deficit detected! Re-weighting scores to prioritize hard deadlines strictly.', 'status': 'running'})}\n\n"
        await asyncio.sleep(1.5)

    plan_str = ", ".join([f"{p['task']} (Score: {p['score']})" for p in plan_data])
    yield f"data: {json.dumps({'agent': 'Planning Agent', 'type': 'action', 'content': f'Ranked Plan: {plan_str}', 'status': 'done'})}\n\n"
    await asyncio.sleep(0.5)

    # Scheduling Agent
    yield f"data: {json.dumps({'agent': 'Scheduling Agent', 'type': 'thought', 'content': 'Attempting to fit blocks into calendar...', 'status': 'running'})}\n\n"
    await asyncio.sleep(1)
    yield f"data: {json.dumps({'agent': 'Scheduling Agent', 'type': 'thought', 'content': 'Conflict deteced: \"Team Sync\" overlaps with requested focus block.', 'status': 'running'})}\n\n"
    await asyncio.sleep(1.5)
    yield f"data: {json.dumps({'agent': 'Scheduling Agent', 'type': 'thought', 'content': 'Conflict resolution: User preferred deep-work tasks have higher matrix score. Shifting \"PPT\" before \"Team Sync\", and truncating \"Demo Recording\".', 'status': 'running'})}\n\n"
    await asyncio.sleep(2)
    yield f"data: {json.dumps({'agent': 'Scheduling Agent', 'type': 'action', 'content': 'Drafted optimized schedule.', 'status': 'done'})}\n\n"
    await asyncio.sleep(0.5)

    # Execution Agent
    yield f"data: {json.dumps({'agent': 'Execution Agent', 'type': 'thought', 'content': 'Writing schedule to Mock Calendar API and Task Manager...', 'status': 'running'})}\n\n"
    await asyncio.sleep(1.5)
    
    # Save to mock DB
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (intent, plan) VALUES (?, ?)", (intent, plan_str))
    conn.commit()
    conn.close()

    yield f"data: {json.dumps({'agent': 'Execution Agent', 'type': 'action', 'content': 'Successfully synced all changes to user tools. Memory updated.', 'status': 'done'})}\n\n"
    yield f"data: {json.dumps({'agent': 'System', 'type': 'end', 'content': 'Workflow Complete.'})}\n\n"

@app.post("/api/plan")
async def plan_workflow(request: QueryRequest):
    return StreamingResponse(mock_agent_stream(request.intent), media_type="text/event-stream")

# Serve React static files
if os.path.isdir("client/dist"):
    app.mount("/assets", StaticFiles(directory="client/dist/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        if full_path != "" and os.path.exists(f"client/dist/{full_path}"):
            return FileResponse(f"client/dist/{full_path}")
        return FileResponse("client/dist/index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
