"""
Performance Monitoring Module for ApexHire
Tracks system performance, memory usage, and processing times
"""

import time
import psutil
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
import tracemalloc

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor system performance and resource usage"""
    
    def __init__(self, output_dir: str = "logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.metrics = []
        self.start_time = None
        self.tracemalloc_start = None
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        self.tracemalloc_start = tracemalloc.start()
        logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        if self.tracemalloc_start:
            tracemalloc.stop()
        logger.info("Performance monitoring stopped")
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'memory_used_gb': memory.used / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get detailed memory usage information"""
        try:
            if self.tracemalloc_start:
                current, peak = tracemalloc.get_traced_memory()
                return {
                    'current_mb': current / 1024 / 1024,
                    'peak_mb': peak / 1024 / 1024,
                    'current_mb_formatted': f"{current / 1024 / 1024:.1f} MB",
                    'peak_mb_formatted': f"{peak / 1024 / 1024:.1f} MB"
                }
            return {}
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return {}
    
    def record_metric(self, operation: str, duration: float, 
                     memory_usage: Optional[Dict] = None, 
                     additional_data: Optional[Dict] = None):
        """Record a performance metric"""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration_seconds': duration,
            'system_metrics': self.get_system_metrics(),
            'memory_usage': memory_usage or self.get_memory_usage(),
            'additional_data': additional_data or {}
        }
        
        self.metrics.append(metric)
        logger.info(f"Performance metric recorded: {operation} took {duration:.2f}s")
        
    def save_metrics(self, filename: str = None):
        """Save metrics to file"""
        if not filename:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    'summary': self.get_summary(),
                    'metrics': self.metrics
                }, f, indent=2)
            
            logger.info(f"Performance metrics saved to: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
            return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics:
            return {}
        
        durations = [m['duration_seconds'] for m in self.metrics]
        operations = [m['operation'] for m in self.metrics]
        
        return {
            'total_operations': len(self.metrics),
            'total_duration': sum(durations),
            'average_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'unique_operations': list(set(operations)),
            'operation_counts': {op: operations.count(op) for op in set(operations)}
        }
    
    def print_summary(self):
        """Print performance summary to console"""
        summary = self.get_summary()
        if not summary:
            print("No performance metrics recorded")
            return
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Total Operations: {summary['total_operations']}")
        print(f"Total Duration: {summary['total_duration']:.2f}s")
        print(f"Average Duration: {summary['average_duration']:.2f}s")
        print(f"Min Duration: {summary['min_duration']:.2f}s")
        print(f"Max Duration: {summary['max_duration']:.2f}s")
        print("\nOperation Breakdown:")
        for op, count in summary['operation_counts'].items():
            print(f"  {op}: {count} times")
        print("="*50)

def monitor_performance(operation_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - monitor.start_time
                
                monitor.record_metric(
                    operation=operation_name or func.__name__,
                    duration=duration,
                    additional_data={'success': True}
                )
                
                return result
            except Exception as e:
                duration = time.time() - monitor.start_time
                monitor.record_metric(
                    operation=operation_name or func.__name__,
                    duration=duration,
                    additional_data={'success': False, 'error': str(e)}
                )
                raise
            finally:
                monitor.stop_monitoring()
        
        return wrapper
    return decorator

def check_system_resources() -> Dict[str, Any]:
    """Check if system has sufficient resources"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        warnings = []
        
        # Check memory
        if memory.percent > 90:
            warnings.append(f"High memory usage: {memory.percent:.1f}%")
        
        # Check disk space
        if disk.percent > 90:
            warnings.append(f"Low disk space: {disk.percent:.1f}% used")
        
        # Check CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:
            warnings.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        return {
            'status': 'warning' if warnings else 'ok',
            'warnings': warnings,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'cpu_percent': cpu_percent
        }
    except Exception as e:
        logger.error(f"Error checking system resources: {e}")
        return {'status': 'error', 'error': str(e)}

# Global performance monitor instance
global_monitor = PerformanceMonitor()

def get_global_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    return global_monitor
