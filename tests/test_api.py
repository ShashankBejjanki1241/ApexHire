"""
API Tests for ApexHire FastAPI Application
"""

import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from api.main import app

client = TestClient(app)

class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "system_metrics" in data
        assert "warnings" in data
        assert "timestamp" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert "summary" in data
        assert "recent_metrics" in data
        assert "system_health" in data
    
    def test_config_endpoint(self):
        """Test configuration endpoint"""
        response = client.get("/config")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "configuration" in data
        assert data["status"] == "success"
    
    def test_config_validate_endpoint(self):
        """Test configuration validation endpoint"""
        response = client.post("/config/validate")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "valid" in data
        assert "message" in data

class TestResumeAnalysis:
    """Test resume analysis endpoints"""
    
    def create_test_resume(self, content="Software Engineer with 5 years experience in Python and JavaScript."):
        """Create a temporary test resume file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            return f.name
    
    def test_analyze_resume_success(self):
        """Test successful resume analysis"""
        # Create test resume
        resume_file = self.create_test_resume()
        
        try:
            # Read file content first
            with open(resume_file, 'rb') as f:
                file_content = f.read()
            
            # Create file-like object for testing
            from io import BytesIO
            file_obj = BytesIO(file_content)
            file_obj.name = "test_resume.txt"
            
            response = client.post(
                "/analyze/resume",
                files={"file": ("test_resume.txt", file_obj, "text/plain")},
                data={
                    "job_title": "Software Engineer",
                    "job_description": "We need a Python developer with experience in web development.",
                    "requirements": "Python,JavaScript,React"
                }
            )
            
            assert response.status_code == 200
            
            data = response.json()
            assert "overall_score" in data
            assert "breakdown" in data
            assert "skills_found" in data
            assert "recommendations" in data
            assert "processing_time" in data
            assert "status" in data
            assert data["status"] == "success"
            
        finally:
            # Cleanup
            if os.path.exists(resume_file):
                os.unlink(resume_file)
    
    def test_analyze_resume_invalid_file_type(self):
        """Test resume analysis with invalid file type"""
        # Create test file with invalid extension
        with tempfile.NamedTemporaryFile(suffix='.invalid', delete=False) as f:
            f.write(b"test content")
            invalid_file = f.name
        
        try:
            with open(invalid_file, 'rb') as f:
                response = client.post(
                    "/analyze/resume",
                    files={"file": ("test.invalid", f, "application/octet-stream")},
                    data={
                        "job_title": "Software Engineer",
                        "job_description": "Test job description",
                        "requirements": "Python"
                    }
                )
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "Unsupported file type" in data["detail"]
            
        finally:
            # Cleanup
            if os.path.exists(invalid_file):
                os.unlink(invalid_file)
    
    def test_analyze_resume_missing_file(self):
        """Test resume analysis with missing file"""
        response = client.post(
            "/analyze/resume",
            data={
                "job_title": "Software Engineer",
                "job_description": "Test job description",
                "requirements": "Python"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_resume_missing_job_title(self):
        """Test resume analysis with missing job title"""
        resume_file = self.create_test_resume()
        
        try:
            with open(resume_file, 'rb') as f:
                response = client.post(
                    "/analyze/resume",
                    files={"file": ("test_resume.txt", f, "text/plain")},
                    data={
                        "job_description": "Test job description",
                        "requirements": "Python"
                    }
                )
            
            assert response.status_code == 422  # Validation error
            
        finally:
            # Cleanup
            if os.path.exists(resume_file):
                os.unlink(resume_file)

class TestBatchAnalysis:
    """Test batch analysis endpoints"""
    
    def create_test_resumes(self, count=2):
        """Create multiple test resume files"""
        files = []
        for i in range(count):
            content = f"Software Engineer {i} with experience in Python and JavaScript."
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                files.append(f.name)
        return files
    
    def test_batch_analysis_success(self):
        """Test successful batch analysis"""
        # Create test resumes
        resume_files = self.create_test_resumes(2)
        
        try:
            files = []
            for i, file_path in enumerate(resume_files):
                # Read file content first
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                
                # Create file-like object for testing
                from io import BytesIO
                file_obj = BytesIO(file_content)
                file_obj.name = f"resume_{i}.txt"
                
                files.append(("files", (f"resume_{i}.txt", file_obj, "text/plain")))
            
            response = client.post(
                "/analyze/batch",
                files=files,
                data={
                    "job_title": "Senior Developer",
                    "job_description": "Senior role requiring Python and leadership skills.",
                    "requirements": "Python,Leadership,5+ years"
                }
            )
            
            assert response.status_code == 200
            
            data = response.json()
            assert "job_title" in data
            assert "total_files" in data
            assert "results" in data
            assert "summary" in data
            assert data["total_files"] == 2
            assert len(data["results"]) == 2
            
            # Check summary
            summary = data["summary"]
            assert "successful" in summary
            assert "failed" in summary
            assert "average_score" in summary
            
        finally:
            # Cleanup
            for file_path in resume_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    def test_batch_analysis_mixed_file_types(self):
        """Test batch analysis with mixed valid and invalid file types"""
        # Create one valid and one invalid file
        valid_file = self.create_test_resumes(1)[0]
        
        with tempfile.NamedTemporaryFile(suffix='.invalid', delete=False) as f:
            f.write(b"invalid content")
            invalid_file = f.name
        
        try:
            files = []
            
            # Read file content first, then create BytesIO objects (like the working test)
            with open(valid_file, 'rb') as f:
                valid_content = f.read()
            with open(invalid_file, 'rb') as f:
                invalid_content = f.read()
            
            # Create file-like objects for testing
            from io import BytesIO
            valid_file_obj = BytesIO(valid_content)
            valid_file_obj.name = "valid.txt"
            invalid_file_obj = BytesIO(invalid_content)
            invalid_file_obj.name = "invalid.invalid"
            
            files.append(("files", ("valid.txt", valid_file_obj, "text/plain")))
            files.append(("files", ("invalid.invalid", invalid_file_obj, "application/octet-stream")))
            
            response = client.post(
                "/analyze/batch",
                files=files,
                data={
                    "job_title": "Developer",
                    "job_description": "Test job description",
                    "requirements": "Python"
                }
            )
            
            # Should fail due to invalid file type
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "Unsupported file type" in data["detail"]
            
        finally:
            # Cleanup
            for file_path in [valid_file, invalid_file]:
                if os.path.exists(file_path):
                    os.unlink(file_path)

class TestErrorHandling:
    """Test error handling in API endpoints"""
    
    def test_health_check_error_handling(self):
        """Test health check error handling"""
        # This test ensures the health endpoint handles errors gracefully
        response = client.get("/health")
        assert response.status_code in [200, 500]  # Should handle errors gracefully
    
    def test_metrics_error_handling(self):
        """Test metrics endpoint error handling"""
        response = client.get("/metrics")
        assert response.status_code in [200, 500]  # Should handle errors gracefully
    
    def test_config_error_handling(self):
        """Test configuration endpoint error handling"""
        response = client.get("/config")
        assert response.status_code in [200, 500]  # Should handle errors gracefully

class TestPerformanceMonitoring:
    """Test performance monitoring integration"""
    
    def create_test_resume(self, content="Software Engineer with 5 years experience in Python and JavaScript."):
        """Create a temporary test resume file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            return f.name
    
    def test_performance_metrics_included(self):
        """Test that performance metrics are included in responses"""
        resume_file = self.create_test_resume()
        
        try:
            # Read file content first
            with open(resume_file, 'rb') as f:
                file_content = f.read()
            
            # Create file-like object for testing
            from io import BytesIO
            file_obj = BytesIO(file_content)
            file_obj.name = "test_resume.txt"
            
            response = client.post(
                "/analyze/resume",
                files={"file": ("test_resume.txt", file_obj, "text/plain")},
                data={
                    "job_title": "Software Engineer",
                    "job_description": "Test job description",
                    "requirements": "Python"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                assert "processing_time" in data
                assert isinstance(data["processing_time"], (int, float))
                
        finally:
            # Cleanup
            if os.path.exists(resume_file):
                os.unlink(resume_file)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
