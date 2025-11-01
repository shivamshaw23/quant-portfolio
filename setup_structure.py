#!/usr/bin/env python3
"""
Setup script to create the Phase I project structure for quant-portfolio.
Run this script to automatically create all necessary directories and starter files.
"""

import os
from pathlib import Path

# Define the project structure
STRUCTURE = {
    "docs": {},
    "configs": {
        "nautilus": {},
        "local.yaml": "# Configuration for local development\n# Add broker credentials here\n",
    },
    "src": {
        "core": {
            "__init__.py": "",
            "event_engine.py": "# Event-driven architecture engine\n",
            "data_handler.py": "# Market data handling\n",
            "order_manager.py": "# Order management system\n",
            "logger.py": "# Logging utilities\n",
        },
        "brokers": {
            "__init__.py": "",
            "binance_client.py": "# Binance Testnet client implementation\n",
            "ibkr_client.py": "# Interactive Brokers client implementation\n",
            "zerodha_sim.py": "# Zerodha simulator/client implementation\n",
        },
        "alphas": {
            "__init__.py": "",
            "alpha_pairs.py": "# Pairs trading alpha strategy\n",
            "alpha_breakout.py": "# Breakout alpha strategy\n",
        },
        "backtest": {"__init__.py": ""},
        "deploy": {"__init__.py": ""},
        "utils": {"__init__.py": ""},
    },
    "tests": {"__init__.py": ""},
    "notebooks": {},
    "results": {},
}


def create_structure(base_path, structure):
    """Recursively create directory structure and files."""
    for name, content in structure.items():
        path = base_path / name
        
        if isinstance(content, dict):
            # It's a directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {path}")
            
            if content:  # If there are sub-items
                create_structure(path, content)
            else:  # Empty directory, create .gitkeep
                gitkeep = path / ".gitkeep"
                gitkeep.write_text("")
                print(f"Created file: {gitkeep}")
        else:
            # It's a file
            path.write_text(content)
            print(f"Created file: {path}")


if __name__ == "__main__":
    print("Setting up quant-portfolio Phase I structure...")
    base = Path(".")
    create_structure(base, STRUCTURE)
    print("\nStructure created successfully!")
    print("\nNext steps:")
    print("1. Review configs/local.yaml and add broker credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start implementing Phase I broker connectivity")
