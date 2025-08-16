"""
FastAPI Application for ApexHire AI Resume Screener
Provides REST API endpoints for resume analysis and job matching
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import logging
import json
import os
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent / "config"))

from main_pipeline import ResumeScreener
from performance_monitor import PerformanceMonitor, check_system_resources
import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ApexHire API",
    description="AI-powered resume screening and job matching API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
screener = ResumeScreener()
performance_monitor = PerformanceMonitor()

# Pydantic models for request/response
class JobDescription(BaseModel):
    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Job description")
    requirements: List[str] = Field(default=[], description="Job requirements")
    preferred_skills: List[str] = Field(default=[], description="Preferred skills")

class ResumeAnalysisRequest(BaseModel):
    job_description: JobDescription
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")

class ResumeAnalysisResponse(BaseModel):
    overall_score: float
    breakdown: Dict[str, Any]
    skills_found: Dict[str, Any]  # Changed to match pipeline output structure
    recommendations: List[str]
    processing_time: float
    status: str

class BatchAnalysisRequest(BaseModel):
    job_description: JobDescription
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")

class SystemHealthResponse(BaseModel):
    status: str
    system_metrics: Dict[str, Any]
    warnings: List[str]
    timestamp: str

class PerformanceMetricsResponse(BaseModel):
    summary: Dict[str, Any]
    recent_metrics: List[Dict[str, Any]]
    system_health: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting ApexHire API...")
    
    # Validate configuration
    if not settings.validate_config():
        logger.error("Configuration validation failed")
        raise Exception("Invalid configuration")
    
    # Check system resources
    health = check_system_resources()
    if health['status'] == 'error':
        logger.error(f"System health check failed: {health.get('error')}")
    
    logger.info("ApexHire API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down ApexHire API...")
    performance_monitor.save_metrics("api_shutdown_metrics.json")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ApexHire AI Resume Screener API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=SystemHealthResponse, tags=["System"])
async def health_check():
    """System health check endpoint"""
    try:
        # Check system resources
        health = check_system_resources()
        
        # Get system metrics
        system_metrics = performance_monitor.get_system_metrics()
        
        return SystemHealthResponse(
            status=health['status'],
            system_metrics=system_metrics,
            warnings=health.get('warnings', []),
            timestamp=system_metrics.get('timestamp', '')
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.get("/metrics", response_model=PerformanceMetricsResponse, tags=["System"])
async def get_performance_metrics():
    """Get performance metrics"""
    try:
        summary = performance_monitor.get_summary()
        recent_metrics = performance_monitor.metrics[-10:] if performance_monitor.metrics else []
        system_health = check_system_resources()
        
        return PerformanceMetricsResponse(
            summary=summary,
            recent_metrics=recent_metrics,
            system_health=system_health
        )
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get metrics")

@app.post("/analyze/resume", response_model=ResumeAnalysisResponse, tags=["Analysis"])
async def analyze_resume(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    requirements: str = Form(default=""),
    background_tasks: BackgroundTasks = None
):
    """
    Analyze a single resume against a job description
    
    - **file**: Resume file (PDF, DOCX, DOC, TXT)
    - **job_title**: Job title
    - **job_description**: Job description
    - **requirements**: Comma-separated requirements
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Start performance monitoring
            performance_monitor.start_monitoring()
            
            # Create job description object
            job_desc = JobDescription(
                title=job_title,
                description=job_description,
                requirements=requirements.split(',') if requirements else []
            )
            
            # Create a temporary job description file
            job_desc_file = f"temp_job_{file.filename}.txt"
            with open(job_desc_file, 'w') as f:
                f.write(f"Job Title: {job_title}\n")
                f.write(f"Job Description: {job_description}\n")
                f.write(f"Requirements: {requirements}\n")
            
            try:
                # Analyze resume
                result = screener.analyze_single_resume(
                    resume_path=temp_file_path,
                    job_path=job_desc_file,
                    output_file=None
                )
            finally:
                # Cleanup job description file
                if os.path.exists(job_desc_file):
                    os.remove(job_desc_file)
            
            # Calculate processing time
            processing_time = performance_monitor.get_memory_usage().get('current_mb', 0)
            
            # Record performance metric
            performance_monitor.record_metric(
                operation="api_resume_analysis",
                duration=processing_time,
                additional_data={
                    "file_type": file_extension,
                    "file_size": len(content),
                    "job_title": job_title
                }
            )
            
            if not result:
                raise HTTPException(status_code=500, detail="Failed to analyze resume")
            
            # Format response
            response = ResumeAnalysisResponse(
                overall_score=result.get('overall_score', 0),
                breakdown=result.get('breakdown', {}),
                skills_found=result.get('skills_found', {}),
                recommendations=result.get('ats_analysis', {}).get('recommendations', []),
                processing_time=processing_time,
                status="success"
            )
            
            return response
            
        finally:
            # Cleanup temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            performance_monitor.stop_monitoring()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/batch", tags=["Analysis"])
async def batch_analysis(
    files: List[UploadFile] = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    requirements: str = Form(default="")
):
    """
    Analyze multiple resumes against a job description
    
    - **files**: List of resume files
    - **job_title**: Job title
    - **job_description**: Job description
    - **requirements**: Comma-separated requirements
    """
    try:
        results = []
        temp_files = []
        
        # Validate and save files
        for file in files:
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in ['.pdf', '.docx', '.doc', '.txt']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type for {file.filename}"
                )
            
            temp_file_path = f"temp_batch_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            temp_files.append(temp_file_path)
        
        try:
            # Start performance monitoring
            performance_monitor.start_monitoring()
            
            # Create job description file
            job_desc_file = "temp_batch_job.txt"
            with open(job_desc_file, 'w') as f:
                f.write(f"Job Title: {job_title}\n")
                f.write(f"Job Description: {job_description}\n")
                f.write(f"Requirements: {requirements}\n")
            
            try:
                # Process each file
                for i, temp_file in enumerate(temp_files):
                    try:
                        result = screener.analyze_single_resume(
                            resume_path=temp_file,
                            job_path=job_desc_file,
                            output_file=None
                        )
                        
                        if result:
                            results.append({
                                "filename": files[i].filename,
                                "overall_score": result.get('overall_score', 0),
                                "skills_found": result.get('skills_found', {}),
                                "status": "success"
                            })
                        else:
                            results.append({
                                "filename": files[i].filename,
                                "status": "failed",
                                "error": "Analysis failed"
                            })
                            
                    except Exception as e:
                        results.append({
                            "filename": files[i].filename,
                            "status": "failed",
                            "error": str(e)
                        })
                
                # Record batch performance
                processing_time = performance_monitor.get_memory_usage().get('current_mb', 0)
                performance_monitor.record_metric(
                    operation="api_batch_analysis",
                    duration=processing_time,
                    additional_data={
                        "files_processed": len(files),
                        "successful_analyses": len([r for r in results if r['status'] == 'success'])
                    }
                )
                
                return {
                    "job_title": job_title,
                    "total_files": len(files),
                    "results": results,
                    "summary": {
                        "successful": len([r for r in results if r['status'] == 'success']),
                        "failed": len([r for r in results if r['status'] == 'failed']),
                        "average_score": sum(r.get('overall_score', 0) for r in results if r['status'] == 'success') / max(len([r for r in results if r['status'] == 'success']), 1)
                    }
                }
            finally:
                # Cleanup job description file
                if os.path.exists(job_desc_file):
                    os.remove(job_desc_file)
            
        finally:
            # Cleanup temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            performance_monitor.stop_monitoring()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@app.get("/config", tags=["System"])
async def get_configuration():
    """Get current configuration"""
    try:
        config = settings.get_config()
        return {
            "status": "success",
            "configuration": config
        }
    except Exception as e:
        logger.error(f"Failed to get configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to get configuration")

@app.post("/config/validate", tags=["System"])
async def validate_configuration():
    """Validate current configuration"""
    try:
        is_valid = settings.validate_config()
        return {
            "status": "success" if is_valid else "error",
            "valid": is_valid,
            "message": "Configuration is valid" if is_valid else "Configuration validation failed"
        }
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise HTTPException(status_code=500, detail="Configuration validation failed")

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.API_CONFIG['host'],
        port=settings.API_CONFIG['port'],
        reload=settings.API_CONFIG['reload'],
        log_level="info"
    )
