"""
Pytest fixtures and test configuration for pyconjpbot2

This module provides common fixtures for testing:
- Database fixtures (in-memory SQLite)
- Mock Slack client
- Test data generators
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
