
from lxml import etree
from copy import deepcopy
E = etree.Element

'''The data structure to store vehicle state'''
class Namespace(dict):
    def __init__(self, *args, **kwargs):
        self.var(*args, **kwargs)

    def var(self, *args, **kwargs):
        kvs = dict()
        for a in args:
            if isinstance(a, str):
                kvs[a] = True
            else: # a is a dictionary
                kvs.update(a)
        kvs.update(kwargs)
        self.update(kvs)
        return self

    def unvar(self, *args):
        for a in args:
            self.pop(a)
        return self

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            self.__getattribute__(key)

    def __setattr__(self, key, value):
        self[key] = value


"""add dynamic obstacle to a commonroad scenarios xml file.

Parameters
----------
input_path(str): the original xml scenrio file 
output_path(str): your output file will be saved here
v_id(str): vehicle id
init_state (Namespace): the initial state of vehicle, includes position(x,y), orientation, time, velocity(float), acceleration(float)
shape(list): the shape of the vehicle, we only support rectangle, the list should contain [length,width]
state_list (a list of Namespace): In CommonRoad, the trajectory is defined as a list of state. 
The required paramters of state_list are same as init_state
"""
def add_dynamic_obs(input_path, output_path, v_id, init_state, shape, state_list):

    def ele_wrapper(id, value):
        wrapper = E('exact')
        wrapper.text = str(value)
        node = E(id)
        node.append(wrapper)
        return node

    tree = etree.parse(input_path)

    root = tree.getroot()
    dynamic_obs =E("dynamicObstacle", id=v_id)
    car_type = E("type") 
    car_type.text = 'car'
    dynamic_obs.append(car_type)
    shape_t = E('shape')
    rectangle = E('rectangle')
    length = E('length')
    length.text = str(shape[0])
    width = E('width')
    width.text = str(shape[1])
    rectangle.append(length)
    rectangle.append(width)
    shape_t.append(rectangle)
    dynamic_obs.append(shape_t)

    ## add initial state information
    initialState = E('initialState')
    iposition = E('position')
    ipoint = E('point')
    ix = E('x')
    ix.text = str(init_state.x)
    iy = E('y')
    iy.text = str(init_state.y)
    ipoint.append(ix)
    ipoint.append(iy)
    iposition.append(ipoint)
    initialState.append(iposition)

    initialState.append(ele_wrapper('orientation', init_state.orientation))
    initialState.append(ele_wrapper('time', init_state.time))
    initialState.append(ele_wrapper('velocity', init_state.velocity))
    initialState.append(ele_wrapper('acceleration', init_state.acceleration))
    dynamic_obs.append(initialState)

    ## add trajectory
    traj_root = E('trajectory')
    for state in state_list:
        state_node = E('state')
        position = E('position')
        point = E('point')
        x = E('x')
        x.text = str(state.x)
        y = E('y')
        y.text = str(state.y)
        point.append(x)
        point.append(y)
        position.append(point)
        state_node.append(position)

        state_node.append(ele_wrapper('orientation', state.orientation))
        state_node.append(ele_wrapper('time', state.time))
        state_node.append(ele_wrapper('velocity', state.velocity))
        state_node.append(ele_wrapper('acceleration', state.acceleration))
        traj_root.append(deepcopy(state_node))
    dynamic_obs.append(traj_root)
    root.append(dynamic_obs)
    etree.ElementTree(root).write(
        output_path, pretty_print=True, encoding='UTF-8', xml_declaration=True)
