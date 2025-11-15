# performers.py — alias module so API imports work

from .best_worst_performer import PerformanceAnalyzer

# Expose exactly what the endpoints expect
get_best_performers = PerformanceAnalyzer.get_best_performers
get_worst_performers = PerformanceAnalyzer.get_worst_performers
