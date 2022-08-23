#!/bin/sh
git clone https://gitlab.lrz.de/tum-cps/commonroad-rl.git
cd commonroad-rl
conda env update --name test --file environment.yml
conda activate test
git submodule init
git submodule update --recursive || exit_with_error "Update submodules failed"
# install third part 
cd external/commonroad-drivability-checker
pip instal -r requirements.txt
git submodule init
git submodule update --recursive
python setup.py install

cd ../commonroad-interactive-scenarios
pip install -r requirements.txt
bash install.sh

# install other requirements
pip install stable_baselines mpi4py optuna pyyaml
