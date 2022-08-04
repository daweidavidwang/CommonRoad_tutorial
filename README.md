# Install Common-Road #
> create a clean conda environment (python==3.7)

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


## Dynamic obstacle example
> install requirement
1. pip install lxml

> examine the static scenario 
2. run dynamic_demo.py

> add dynamic obstacle to ZAM_Tutorial-1_1_no_obs.xml
3. run dynamic_obstable_example,py

> There will be a new generated file named "output.xml"
4. modify the first line of dynamic_demo.py to "output.xml"

> run demo again, you will see a moving vehicle in this scenario 
5. run dynamic_demo.py