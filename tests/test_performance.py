"""
Performance tests for ApexHire
"""

import pytest
import time
import tempfile
import os
from pathlib import Path
from src.performance_monitor import PerformanceMonitor, check_system_resources
from src.main_pipeline import ResumeScreener

class TestPerformance:
    """Performance test cases"""
    
    def test_performance_monitor_initialization(self):
        """Test performance monitor initialization"""
        monitor = PerformanceMonitor()
        assert monitor is not None
        assert monitor.metrics == []
    
    def test_system_resources_check(self):
        """Test system resources check"""
        resources = check_system_resources()
        assert 'status' in resources
        assert 'memory_percent' in resources
        assert 'disk_percent' in resources
        assert 'cpu_percent' in resources
    
    def test_performance_metric_recording(self):
        """Test recording performance metrics"""
        monitor = PerformanceMonitor()
        monitor.start_monitoring()
        
        # Simulate some work
        time.sleep(0.1)
        
        monitor.record_metric(
            operation="test_operation",
            duration=0.1,
            additional_data={"test": True}
        )
        
        assert len(monitor.metrics) == 1
        assert monitor.metrics[0]['operation'] == "test_operation"
        assert monitor.metrics[0]['duration_seconds'] == 0.1
    
    def test_performance_summary(self):
        """Test performance summary generation"""
        monitor = PerformanceMonitor()
        
        # Add some test metrics
        monitor.record_metric("op1", 1.0)
        monitor.record_metric("op2", 2.0)
        monitor.record_metric("op1", 1.5)
        
        summary = monitor.get_summary()
        
        assert summary['total_operations'] == 3
        assert summary['total_duration'] == 4.5
        assert summary['average_duration'] == 1.5
        assert summary['min_duration'] == 1.0
        assert summary['max_duration'] == 2.0
        assert 'op1' in summary['unique_operations']
        assert 'op2' in summary['unique_operations']
    
    def test_metrics_saving(self):
        """Test saving metrics to file"""
        monitor = PerformanceMonitor(output_dir="test_logs")
        monitor.record_metric("test_op", 1.0)
        
        filename = monitor.save_metrics("test_metrics.json")
        assert filename is not None
        assert os.path.exists(filename)
        
        # Cleanup
        os.remove(filename)
        os.rmdir("test_logs")
    
    @pytest.mark.slow
    def test_resume_processing_performance(self):
        """Test resume processing performance"""
        screener = ResumeScreener()
        monitor = PerformanceMonitor()
        
        # Create a test resume file
        test_content = "Software Engineer with 5 years experience in Python, JavaScript, and React."
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            monitor.start_monitoring()
            
            # Process the resume
            result = screener.analyze_resume(test_file)
            
            duration = time.time() - monitor.start_time
            monitor.record_metric("resume_analysis", duration)
            
            # Performance assertions
            assert duration < 10.0  # Should complete within 10 seconds
            assert result is not None
            assert 'skills' in result
            
            summary = monitor.get_summary()
            assert summary['total_operations'] == 1
            assert summary['average_duration'] < 10.0
            
        finally:
            monitor.stop_monitoring()
            os.unlink(test_file)
    
    def test_memory_usage_tracking(self):
        """Test memory usage tracking"""
        monitor = PerformanceMonitor()
        monitor.start_monitoring()
        
        # Simulate memory usage
        large_list = [i for i in range(100000)]
        
        memory_usage = monitor.get_memory_usage()
        monitor.stop_monitoring()
        
        # Memory usage should be tracked
        assert 'current_mb' in memory_usage or memory_usage == {}
    
    def test_concurrent_processing(self):
        """Test concurrent processing performance"""
        screener = ResumeScreener()
        monitor = PerformanceMonitor()
        
        # Create multiple test files
        test_files = []
        for i in range(3):
            content = f"Software Engineer {i} with experience in Python and JavaScript."
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            monitor.start_monitoring()
            
            # Process files sequentially
            results = []
            for file in test_files:
                result = screener.analyze_resume(file)
                results.append(result)
            
            duration = time.time() - monitor.start_time
            monitor.record_metric("batch_processing", duration)
            
            # Performance assertions
            assert len(results) == 3
            assert all(result is not None for result in results)
            assert duration < 30.0  # Should complete within 30 seconds
            
        finally:
            monitor.stop_monitoring()
            for file in test_files:
                os.unlink(file)
    
    def test_error_handling_performance(self):
        """Test performance monitoring with errors"""
        monitor = PerformanceMonitor()
        monitor.start_monitoring()
        
        try:
            # Simulate an error
            raise ValueError("Test error")
        except ValueError:
            duration = time.time() - monitor.start_time
            monitor.record_metric(
                "error_operation",
                duration,
                additional_data={"success": False, "error": "Test error"}
            )
        
        monitor.stop_monitoring()
        
        assert len(monitor.metrics) == 1
        metric = monitor.metrics[0]
        assert metric['operation'] == "error_operation"
        assert metric['additional_data']['success'] == False
        assert metric['additional_data']['error'] == "Test error"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
