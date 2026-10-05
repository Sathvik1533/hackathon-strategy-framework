#!/usr/bin/env python3
"""
CLI wrapper for Orbit Mascot Agent
Usage:
  python3 scripts/mascot_agent.py "Your problem statement here"
"""

import os
import sys

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_layer.mascot_agent import main

if __name__ == "__main__":
    main()
