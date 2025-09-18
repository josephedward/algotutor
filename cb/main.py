"""Main entry point for CB Algorithm Tutor."""

import sys
import os
from pathlib import Path

# Add the package directory to Python path
package_dir = Path(__file__).parent
sys.path.insert(0, str(package_dir))

from cb.cli.main import main

if __name__ == "__main__":
    main()