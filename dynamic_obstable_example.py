from dynamic_obstacle_writer import add_dynamic_obs, Namespace
from lxml import etree
from copy import deepcopy

def parse_and_write_new(obs_dir, orignal_xml, output_dir):
    
    tree = etree.parse(obs_dir)

    root = tree.getroot()
    shape = [root.find('shape').find('rectangle').find('length').text, root.find('shape').find('rectangle').find('width').text]
    init_state_node = root.find('initialState')
    initstate = Namespace(
        x = init_state_node.find('position').find('point').find('x').text,
        y = init_state_node.find('position').find('point').find('y').text,
        orientation = init_state_node.find('orientation').find('exact').text,
        time = init_state_node.find('time').find('exact').text,
        velocity = init_state_node.find('velocity').find('exact').text,
        acceleration = init_state_node.find('acceleration').find('exact').text
    )
    traj_node = root.find('trajectory')
    state_list = []
    for state_node in traj_node.findall('state'):
        state = Namespace(
            x = state_node.find('position').find('point').find('x').text,
            y = state_node.find('position').find('point').find('y').text,
            orientation = state_node.find('orientation').find('exact').text,
            time = state_node.find('time').find('exact').text,
            velocity = state_node.find('velocity').find('exact').text,
            acceleration = state_node.find('acceleration').find('exact').text
        )
        state_list.extend([deepcopy(state)])

    add_dynamic_obs(orignal_xml, output_dir, '11', initstate, shape, state_list)



parse_and_write_new("obs.xml", "ZAM_Tutorial-1_1_no_obs.xml","output.xml")