# Install Common-Road #
> pip install commonroad-all

> git clone https://gitlab.lrz.de/tum-cps/commonroad-scenario-designer.git

> cd commonroad-scenario-designer 

> conda install -c conda-forge cartopy

> pip install -r requirements.txt && python setup.py install 

# Run example
## Map Convert From OpenDRIVE format
1. run python file "opendrive_converter.py"
> Opendrive_converter.py is used to convert OpenDRIVE map to CommonRoad scenario XML file

> modify the first two line in Opendrive_converter.py to try with your OpenDRIVE file 
2. run python file opendrive_demo.py
> opendrive_demo.py parses the XML scenario file and renders it with Matplotlib.

> modify the second line in opendrive_demo.py to run other scenario

## Planning example
> install commonroad planning pack first
1. git clone https://gitlab.lrz.de/tum-cps/commonroad-search.git

2. cd commonroad-search && pip install -r requirements.txt

3. run python file planning_example.py
> The black point denotes the vehicle's position. 