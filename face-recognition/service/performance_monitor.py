# ===== PERFORMANCE MONITORING =====
# File: face_api/service/performance_monitor.py
# Mục đích: Theo dõi hiệu suất FAISS operations

import time
import functools
import threading
from typing import Dict, List
from collections import defaultdict, deque

class PerformanceMonitor:
    """Theo dõi hiệu suất các operations"""
    
    def __init__(self):
        self.stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
            'max_time': 0.0,
            'min_time': float('inf'),
            'recent_times': deque(maxlen=10)  # 10 lần gần nhất
        })
        self._lock = threading.Lock()
    
    def track_operation(self, operation_name: str):
        """Decorator để track thời gian operation"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self._record_stats(operation_name, duration)
            return wrapper
        return decorator
    
    def _record_stats(self, operation_name: str, duration: float):
        """Ghi lại thống kê performance"""
        with self._lock:
            stats = self.stats[operation_name]
            stats['count'] += 1
            stats['total_time'] += duration
            stats['avg_time'] = stats['total_time'] / stats['count']
            stats['max_time'] = max(stats['max_time'], duration)
            stats['min_time'] = min(stats['min_time'], duration)
            stats['recent_times'].append(duration)
    
    def get_stats(self) -> Dict:
        """Lấy thống kê hiệu suất"""
        with self._lock:
            return {
                operation: {
                    'count': stats['count'],
                    'avg_time_ms': round(stats['avg_time'] * 1000, 2),
                    'max_time_ms': round(stats['max_time'] * 1000, 2),
                    'min_time_ms': round(stats['min_time'] * 1000, 2),
                    'recent_avg_ms': round(
                        sum(stats['recent_times']) / len(stats['recent_times']) * 1000, 2
                    ) if stats['recent_times'] else 0
                }
                for operation, stats in self.stats.items()
            }
    
    def get_summary(self) -> str:
        """Lấy tóm tắt performance"""
        stats = self.get_stats()
        summary = ["📊 FAISS Performance Summary:"]
        
        for operation, data in stats.items():
            summary.append(
                f"  • {operation}: {data['count']} calls, "
                f"avg: {data['avg_time_ms']}ms, "
                f"recent avg: {data['recent_avg_ms']}ms"
            )
        
        return "\n".join(summary)

# Global monitor instance
performance_monitor = PerformanceMonitor()

# Convenience functions
def track_operation(operation_name: str):
    return performance_monitor.track_operation(operation_name)

def get_performance_stats():
    return performance_monitor.get_stats()

def get_performance_summary():
    return performance_monitor.get_summary()
