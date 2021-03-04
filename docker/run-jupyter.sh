#!/bin/bash

# This script becomes a command available within the Docker environment. Run it, and bash will print a URL which, pasted into the browser, provides a Jupyter environment.

/opt/conda/bin/jupyter notebook --notebook-dir=/mnt/tax.co --ip='0.0.0.0' --port=8888 --no-browser --allow-root
