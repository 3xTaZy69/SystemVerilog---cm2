import pyperclip
import math

scene_blocks = {}
scene_connections = []
d_ff_count = 0
class block:
    """
    block
    """
    def __init__(self, index: int, x: int, y: int, z: int, params: list[int], name: str):
        self.index = str(index)
        self.x = str(x)
        self.y = str(y)
        self.z = str(z)
        self.params = [str(i) for i in params]
        self.world_name = name
        self.calculate_final_look()
        self.add_to_blocks()
    
    def add_to_blocks(self):
        global scene_blocks
        scene_blocks[len(scene_blocks)] = self

    def calculate_final_look(self):
        if not self.params:
            self.final_look = ",".join([self.index, "0", self.x, self.y, self.z])+",;"
        else:
            self.final_look = ",".join([self.index, "0", self.x, self.y, self.z, "+".join(self.params)])+";"




class PD_ff:
    """
    Orientation counter-clockwise
    start_pos - x, y, z
    positive edge d flip flop
    """
    def __init__(self, orientation: int, start_pos: list[int], input_block: block):
        global d_ff_count
        self.blocks = {}
        self.connections = []
        self.type = "posedge"
        self.index = d_ff_count
        if orientation == 0:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]+1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]+2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]+3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]+4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
        elif orientation == 90:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]-1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]-2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]-3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]-4, [], f"d_ff_2node{d_ff_count}")
        elif orientation == 180:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]-1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]-2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]-3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]-4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
        elif orientation == 270:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]+1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]+2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]+3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]+4, [], f"d_ff_2node{d_ff_count}")

        self.connections.append(scene_connection(f"d_ff_node{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_xor{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_and{d_ff_count}", f"d_ff_t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_2node{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(input_block.world_name, f"d_ff_node{d_ff_count}"))
        d_ff_count += 1
        self.point_to_scene()

    def point_to_scene(self):
        global scene_connections
        for connection in self.connections:
            scene_connections.append(connection)

class ND_ff:
    """
    Orientation counter-clockwise
    start_pos - x, y, z
    negative edge d flip flop
    """
    def __init__(self, orientation: int, start_pos: list[int], input_block: block):
        global d_ff_count
        self.blocks = {}
        self.connections = []
        self.type = "negedge"
        self.index = d_ff_count
        if orientation == 0:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]+1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]+2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]+3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]+4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0]+5, start_pos[1], start_pos[2], [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0]+6, start_pos[1], start_pos[2], [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0]+7, start_pos[1], start_pos[2], [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0]+8, start_pos[1], start_pos[2], [], f"d_ff_2and{d_ff_count}")
        elif orientation == 90:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]-1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]-2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]-3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]-4, [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0], start_pos[1], start_pos[2]-5, [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0], start_pos[1], start_pos[2]-6, [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0], start_pos[1], start_pos[2]-7, [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0], start_pos[1], start_pos[2]-8, [], f"d_ff_2and{d_ff_count}")
        elif orientation == 180:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]-1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]-2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]-3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]-4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0]-5, start_pos[1], start_pos[2], [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0]-6, start_pos[1], start_pos[2], [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0]-7, start_pos[1], start_pos[2], [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0]-8, start_pos[1], start_pos[2], [], f"d_ff_2and{d_ff_count}")
        elif orientation == 270:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]+1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]+2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]+3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]+4, [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0], start_pos[1], start_pos[2]+5, [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0], start_pos[1], start_pos[2]+6, [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0], start_pos[1], start_pos[2]+7, [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0], start_pos[1], start_pos[2]+8, [], f"d_ff_2and{d_ff_count}")

        self.connections.append(scene_connection(f"d_ff_node{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_xor{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_and{d_ff_count}", f"d_ff_t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_2node{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_inode{d_ff_count}", f"d_ff_2t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_inode{d_ff_count}", f"d_ff_not{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_not{d_ff_count}", f"d_ff_2and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2t_ff{d_ff_count}", f"d_ff_2and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2and{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2and{d_ff_count}", f"d_ff_2t_ff{d_ff_count}"))
        self.connections.append(scene_connection(input_block.world_name, f"d_ff_node{d_ff_count}"))
        d_ff_count += 1
        self.point_to_scene()

    def point_to_scene(self):
        global scene_connections
        for connection in self.connections:
            scene_connections.append(connection)

class scene_connection:
    """
    connection
    """
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst


output_code_blocks = ""
output_code_connections = ""

def build_scene():
    """
    builds scene
    """
    global scene_blocks, scene_connections, output_code_connections, output_code_blocks, end_time
    for connection in scene_connections:
        try:
            output_code_connections += [str(index+1) for index, block_ in scene_blocks.items() if block_.world_name == connection.src][0]
            output_code_connections += ","
            output_code_connections += [str(index+1) for index, block_ in scene_blocks.items() if block_.world_name == connection.dst][0]
            output_code_connections += ";"
        except:
            raise NameError(connection.src, connection.dst)
    
    for index, block_ in scene_blocks.items():
        output_code_blocks += block_.final_look

    copy_or_print = input("Copy or print: ").lower()
    if copy_or_print == "print":
        print(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")
    else:
        pyperclip.copy(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")

class always_relay_on:
    """
    makes a d flip flop relay on some block like clock etc.
    """
    def __init__(self, block_to_relay_on, d_ff, output_block):
        if d_ff.type == "posedge":
            scene_connections.append(scene_connection(block_to_relay_on.world_name, f"d_ff_and{d_ff.index}"))
            scene_connections.append(scene_connection(f"d_ff_t_ff{d_ff.index}", output_block.world_name))
        elif d_ff.type == "negedge":
            scene_connections.append(scene_connection(block_to_relay_on.world_name, f"d_ff_inode{d_ff.index}"))
            scene_connections.append(scene_connection(f"d_ff_2node{d_ff.index}", output_block.world_name))

and_gate_count = 0
def and_gate(input1, input2, position: list[int]):
    """
    and gate
    """
    global scene_connections, scene_blocks, and_gate_count

    gate = block(1, position[0], position[1], position[2], [], f"and_gate{and_gate_count}")
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    and_gate_count += 1

    return gate

not_gate_count = 0
def not_gate(input, position: list[int]):
    """
    not gate
    """
    global scene_connections, scene_blocks, not_gate_count

    gate = block(0, position[0], position[1], position[2], [], f"not_gate{not_gate_count}")
    scene_connections.append(scene_connection(input, gate.world_name))
    not_gate_count += 1

    return gate

or_gate_count = 0
def or_gate(input1, input2, position: list[int]):
    """
    or gate
    """
    global scene_connections, scene_blocks, or_gate_count

    gate = block(2, position[0], position[1], position[2], [], f"or_gate{or_gate_count}")
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    or_gate_count += 1

    return gate

xor_gate_count = 0
def xor_gate(input1, input2, position: list[int]):
    """
    xor gate
    """
    global scene_connections, scene_blocks, xor_gate_count

    gate = block(3, position[0], position[1], position[2], [], f"xor_gate{xor_gate_count}")
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    xor_gate_count += 1

    return gate

nor_gate_count = 0
def nor_gate(input1, input2, position: list[int]):
    """
    nor gate
    """
    global scene_connections, scene_blocks, nor_gate_count

    gate = block(0, position[0], position[1], position[2], [], f"nor_gate{nor_gate_count}")
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    nor_gate_count += 1

    return gate


logics = 0
def logic(start_pos: list[int], end_pos: list[int], width: int, block_type: int):
    """
    generation of busses
    """
    global logics
    step = [(end_pos[i] - start_pos[i]) // max(1, width-1) for i in range(3)]
    blocks = []

    for b in range(width):
        pos = [start_pos[i] + step[i]*b for i in range(3)]
        blocks.append(block(block_type, pos[0], pos[1], pos[2], [], f"logic_{b}_{logics}"))

    logics += 1
    return blocks

r_adders = 0
def ripple_adder(start_pos: list[int], width: int, type: str):
    """
    type: add for adding, sub for subtracting 
    dynamic generation of ripple adders
    """
    global r_adders, scene_connections, scene_blocks

    blocks = []
    connections = []

    for bit in range(width):
        x = start_pos[0]+bit*(-2)
        y = start_pos[1]
        z = start_pos[2]

        blocks.append(block(15, str(x), str(y), str(z), [], f"r_adder_A_{bit}_{r_adders}"))
        if type == "add":
            blocks.append(block(15, str(x+1), str(y), str(z), [], f"r_adder_B_{bit}_{r_adders}"))
            blocks.append(block(15, str(x+1), str(y), str(z+1), [], f"r_adder_Cin_{bit}_{r_adders}"))
        elif type == "sub": 
            blocks.append(block(0, str(x+1), str(y), str(z), [], f"r_adder_B_{bit}_{r_adders}"))
            if bit == 0:
                blocks.append(block(0, str(x+1), str(y), str(z+1), [], f"r_adder_Cin_{bit}_{r_adders}"))
            else: 
                blocks.append(block(15, str(x+1), str(y), str(z+1), [], f"r_adder_Cin_{bit}_{r_adders}"))
            
        blocks.append(block(3, str(x), str(y), str(z-1), [], f"r_adder_XOR0_{bit}_{r_adders}"))
        blocks.append(block(1, str(x), str(y), str(z-2), [], f"r_adder_AND0_{bit}_{r_adders}"))
        blocks.append(block(15, str(x), str(y), str(z-3), [], f"r_adder_Cout_{bit}_{r_adders}"))
        blocks.append(block(3, str(x+1), str(y), str(z-1), [], f"r_adder_XOR1_{bit}_{r_adders}"))
        blocks.append(block(1, str(x+1), str(y), str(z-2), [], f"r_adder_AND1_{bit}_{r_adders}"))
        blocks.append(block(15, str(x+1), str(y), str(z-4), [], f"r_adder_C_{bit}_{r_adders}"))

        connections.append(scene_connection(f"r_adder_A_{bit}_{r_adders}", f"r_adder_XOR0_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_B_{bit}_{r_adders}", f"r_adder_XOR0_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_A_{bit}_{r_adders}", f"r_adder_AND0_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_B_{bit}_{r_adders}", f"r_adder_AND0_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_AND0_{bit}_{r_adders}", f"r_adder_Cout_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_XOR0_{bit}_{r_adders}", f"r_adder_XOR1_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_XOR0_{bit}_{r_adders}", f"r_adder_AND1_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_Cin_{bit}_{r_adders}", f"r_adder_XOR1_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_Cin_{bit}_{r_adders}", f"r_adder_AND1_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_AND1_{bit}_{r_adders}", f"r_adder_Cout_{bit}_{r_adders}"))
        connections.append(scene_connection(f"r_adder_XOR1_{bit}_{r_adders}", f"r_adder_C_{bit}_{r_adders}"))

        if bit > 0:
            connections.append(scene_connection(f"r_adder_Cout_{bit-1}_{r_adders}", f"r_adder_Cin_{bit}_{r_adders}"))

    for connection in connections:
        scene_connections.append(connection)

    r_adders += 1

    return [b for b in blocks if (b.world_name.startswith("r_adder_A_") or b.world_name.startswith("r_adder_B_") or b.world_name.startswith("r_adder_C_"))]

mux_i_count = 0
def mux_i(inputs: list, inputs_width: int, position: list[int]):
    """
    dynamic generation of muxes with choises of inputs
    """
    x = position[0]
    y = position[1]
    z = position[2]
    max_index = len(inputs)
    sel_len = math.ceil(math.log(max_index, 2))
    select = logic([x, y, z], [x+sel_len-1, y, z], sel_len, 15)
    nselect = logic([x, y, z+1], [x+sel_len, y, z+1], sel_len, 0)
    for i in range(sel_len):
        scene_connections.append(scene_connection(select[i].world_name, nselect[i].world_name))
    output_logic = logic([x, y, z+3], [x+inputs_width, y, z+3], inputs_width, 15)

    for index, input_ in enumerate(inputs):
        b_index = bin(index)[2:].zfill(sel_len)
        x = position[0]+index*inputs_width+sel_len
        a_input = logic([x, y, z+2], [x+inputs_width, y, z+2], inputs_width, 1)
        for index_, bit in enumerate(a_input):
            for i, n in enumerate(b_index):
                if n == "0":
                    scene_connections.append(scene_connection(nselect[i].world_name, bit.world_name))
                else:
                    scene_connections.append(scene_connection(select[i].world_name, bit.world_name))
            scene_connections.append(scene_connection(bit.world_name, output_logic[index_].world_name))
            scene_connections.append(scene_connection(input_[index_].world_name, bit.world_name))
    mux_i_count += 1
    return select, output_logic

mux_c_count = 0
def mux_c(inputs: list, inputs_width: int, position: list[int]):
    """
    dynamic generation of decoding muxes with const choises
    """
    x = position[0]
    y = position[1]
    z = position[2]
    max_index = len(inputs)
    sel_len = math.ceil(math.log(max_index, 2))
    select = logic([x, y, z], [x+sel_len-1, y, z], sel_len, 15)
    nselect = logic([x, y, z+1], [x+sel_len, y, z+1], sel_len, 0)
    for i in range(sel_len):
        scene_connections.append(scene_connection(select[i].world_name, nselect[i].world_name))
    output_logic = logic([x, y, z+3], [x+inputs_width, y, z+3], inputs_width, 15)

    inputs_ = []
    for i, input_ in enumerate(inputs):
        inputs_.append([])
        for ibit, bit in enumerate(input_):
            x = position[0]+i*inputs_width+sel_len+ibit
            if bit == "0":
                inputs_[i].append(block(0, x, y, z-1, [], f"inputs__{bit}_{i}_{mux_c_count}"))
            else:
                inputs_[i].append(block(15, x, y, z-1, [], f"inputs__{bit}_{i}_{mux_c_count}"))

    for index, input_ in enumerate(inputs_):
        b_index = bin(index)[2:].zfill(sel_len)
        x = position[0]+index*inputs_width+sel_len
        a_input = logic([x, y, z+2], [x+inputs_width, y, z+2], inputs_width, 1)
        for index_, bit in enumerate(a_input):
            for i, n in enumerate(b_index):
                if n == "0":
                    scene_connections.append(scene_connection(nselect[i].world_name, bit.world_name))
                else:
                    scene_connections.append(scene_connection(select[i].world_name, bit.world_name))
            scene_connections.append(scene_connection(bit.world_name, output_logic[index_].world_name))
            scene_connections.append(scene_connection(input_[index_].world_name, bit.world_name))
    mux_c_count += 1
    return select, output_logic

build_scene()
