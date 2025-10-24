"""
DionoAutogen AI - Main FastAPI Application
Autonomous Software Architect & Data-Science Engineering Platform
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Optional, Dict, Any
import asyncio
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

from .config import settings, get_workspace_path
from .models import (
    BuildPlanRequest, BuildPlanResponse,
    CodeExecutionRequest, CodeExecutionResponse,
    DeploymentRequest, DeploymentResponse,
    WebSocketMessage, TaskStatus, ProjectInfo
)
from .llm_wrapper import llm
from .sandbox_runner import sandbox
from .ingestion import ingestion
from .auth import get_current_user, authenticate_user, create_access_token
from .cloud_drives import get_cloud_client, CloudProvider

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Autonomous Software Architect & Data-Science Engineering Platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        # Note: Currently supports one WebSocket per session_id (last connection wins)
        # For multiple connections per session, change to Dict[str, List[WebSocket]]
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected: {session_id}")
    
    async def send_message(self, session_id: str, message: WebSocketMessage):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message.dict())
            except Exception as e:
                logger.error(f"Failed to send message to {session_id}: {e}")
    
    async def broadcast(self, message: WebSocketMessage):
        for session_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message.dict())
            except Exception as e:
                logger.error(f"Failed to broadcast to {session_id}: {e}")

manager = ConnectionManager()


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


# Authentication endpoints
@app.post("/api/token")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login and get access token"""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["user_id"], "username": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# Build plan endpoint
@app.post(f"{settings.API_PREFIX}/plan", response_model=BuildPlanResponse)
async def generate_plan(
    request: BuildPlanRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate a build plan from natural language description"""
    try:
        logger.info(f"Generating plan for: {request.project_name}")
        
        # Generate plan using LLM
        plan_data = await llm.generate_plan(
            description=request.description,
            requirements=request.requirements
        )
        
        # Create workspace
        workspace = get_workspace_path(request.project_name)
        
        response = BuildPlanResponse(
            project_name=request.project_name,
            description=request.description,
            steps=plan_data.get("steps", []),
            estimated_time=plan_data.get("estimated_time", 60),
            tech_stack=plan_data.get("tech_stack", []),
            file_structure=plan_data.get("file_structure", {})
        )
        
        # Save plan to workspace
        plan_file = Path(workspace) / "build_plan.json"
        plan_file.write_text(json.dumps(response.dict(), indent=2))
        
        return response
    
    except Exception as e:
        logger.error(f"Plan generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Code execution endpoint
@app.post(f"{settings.API_PREFIX}/run", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Execute code in secure sandbox"""
    try:
        logger.info(f"Executing {request.language} code for: {request.project_name}")
        
        workspace = get_workspace_path(request.project_name)
        
        result = await sandbox.execute(
            code=request.code,
            language=request.language,
            timeout=request.timeout,
            workspace=workspace
        )
        
        return result
    
    except Exception as e:
        logger.error(f"Code execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Deployment endpoint
@app.post(f"{settings.API_PREFIX}/deploy", response_model=DeploymentResponse)
async def deploy_application(
    request: DeploymentRequest,
    current_user: dict = Depends(get_current_user)
):
    """Deploy application"""
    try:
        logger.info(f"Deploying: {request.project_name}")
        
        workspace = get_workspace_path(request.project_name)
        
        # TODO: Implement actual deployment logic
        # For now, return success with placeholder
        
        return DeploymentResponse(
            success=True,
            deployment_url=f"http://localhost:8080/{request.project_name}",
            message="Deployment initiated successfully",
            logs="Deployment in progress..."
        )
    
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# File upload endpoint
@app.post(f"{settings.API_PREFIX}/upload")
async def upload_files(
    project_name: str = Form(...),
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload files to project workspace"""
    try:
        workspace = get_workspace_path(project_name)
        uploaded_files = []
        
        for file in files:
            file_path = Path(workspace) / file.filename
            content = await file.read()
            file_path.write_bytes(content)
            
            uploaded_files.append({
                "name": file.filename,
                "size": len(content),
                "path": str(file_path.relative_to(workspace))
            })
        
        return {
            "success": True,
            "message": f"Uploaded {len(uploaded_files)} files",
            "files": uploaded_files
        }
    
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Project info endpoint
@app.get(f"{settings.API_PREFIX}/projects/{{project_name}}", response_model=ProjectInfo)
async def get_project_info(
    project_name: str,
    current_user: dict = Depends(get_current_user)
):
    """Get project information"""
    try:
        workspace = Path(get_workspace_path(project_name))
        
        if not workspace.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get all files
        files = [str(f.relative_to(workspace)) for f in workspace.rglob("*") if f.is_file()]
        
        # Calculate total size
        total_size = sum(f.stat().st_size for f in workspace.rglob("*") if f.is_file())
        
        # Get timestamps
        created_at = datetime.fromtimestamp(workspace.stat().st_ctime)
        updated_at = datetime.fromtimestamp(workspace.stat().st_mtime)
        
        return ProjectInfo(
            name=project_name,
            description="",  # TODO: Load from metadata
            created_at=created_at,
            updated_at=updated_at,
            status=TaskStatus.COMPLETED,  # TODO: Track actual status
            files=files,
            size_mb=total_size / (1024 * 1024)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# List projects endpoint
@app.get(f"{settings.API_PREFIX}/projects")
async def list_projects(current_user: dict = Depends(get_current_user)):
    """List all projects"""
    try:
        workspace_dir = Path(settings.WORKSPACE_DIR)
        workspace_dir.mkdir(exist_ok=True)
        
        projects = []
        for project_path in workspace_dir.iterdir():
            if project_path.is_dir():
                projects.append({
                    "name": project_path.name,
                    "created_at": datetime.fromtimestamp(project_path.stat().st_ctime).isoformat(),
                    "updated_at": datetime.fromtimestamp(project_path.stat().st_mtime).isoformat()
                })
        
        return {"projects": projects}
    
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(session_id, websocket)
    
    try:
        # Send welcome message
        await manager.send_message(
            session_id,
            WebSocketMessage(
                type="status",
                status=TaskStatus.PLANNING,
                message="Connected to DionoAutogen AI"
            )
        )
        
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            
            # Process message
            message_type = data.get("type")
            
            if message_type == "ping":
                await manager.send_message(
                    session_id,
                    WebSocketMessage(type="pong", message="pong")
                )
            
            elif message_type == "execute":
                # Execute code and stream results
                code = data.get("code", "")
                language = data.get("language", "python")
                project_name = data.get("project_name", "default")
                
                await manager.send_message(
                    session_id,
                    WebSocketMessage(
                        type="status",
                        status=TaskStatus.CODING,
                        message="Executing code..."
                    )
                )
                
                workspace = get_workspace_path(project_name)
                result = await sandbox.execute(code, language, workspace=workspace)
                
                await manager.send_message(
                    session_id,
                    WebSocketMessage(
                        type="result",
                        message="Execution completed",
                        data=result.dict()
                    )
                )
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}")
        manager.disconnect(session_id)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Create workspace directory
    Path(settings.WORKSPACE_DIR).mkdir(exist_ok=True)
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    logger.info("Application started successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")
    
    # Cleanup sandbox
    sandbox.cleanup()
    
    # Close LLM client
    await llm.close()
    
    logger.info("Application shutdown complete")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
