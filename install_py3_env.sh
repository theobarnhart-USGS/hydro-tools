conda config --prepend channels conda-forge
conda config --set channel_priority strict

conda env create -f path-to-env-file-here
