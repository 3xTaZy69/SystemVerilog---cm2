import pyperclip
import math
conf = {
    "grid_type": "cube",
    "extra": "",
    "CopyOrPrint": "print"
}


scene_blocks_i = {}
scene_blocks_n = []
scene_connections = []
d_ff_count = 0
class block:
    """
    block
    """
    def __init__(self, index: int, x: int, y: int, z: int, params: list[int], name: str, not_add_block_to_blocks=None, no_formatting=False):
        self.index = str(index)
        self.x = str(x)
        self.y = str(y)
        self.z = str(z)
        self.params = [str(i) for i in params]
        self.world_name = name
        self.calculate_final_look()
        self.no_formatting = no_formatting
        if not not_add_block_to_blocks:
            self.add_to_blocks()
    
    def add_to_blocks(self):
        global scene_blocks_n, scene_blocks_i, blocks_not_to_format
        scene_blocks_i[len(scene_blocks_i)] = self
        scene_blocks_n.append(self)
        if self.no_formatting:
            blocks_not_to_format.append(self)
            

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

def build_scene_no_formatting():
    """
    builds scene
    """
    global scene_blocks, scene_connections, output_code_connections, output_code_blocks, end_time
    for connection in scene_connections:
        try:
            output_code_connections += str(scene_blocks_n.index(connection.src) + 1)
            output_code_connections += ","
            output_code_connections += str(scene_blocks_n.index(connection.dst) + 1)
            output_code_connections += ";"
        except:
            raise NameError(connection.src, connection.dst)
        
    for index, block_ in scene_blocks_i.items():
        output_code_blocks += block_.final_look

    copy_or_print = conf["CopyOrPrint"]
    if copy_or_print == "print":
        print(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")
    else:
        pyperclip.copy(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")

blocks_not_to_format = []
not_formatted_code = ""
def build_scene():
    """
    builds scene
    """
    global scene_blocks_n, scene_connections, output_code_connections, output_code_blocks, end_time, blocks_not_to_format, not_formatted_code
    blocks_not_to_format_names = [b.world_name for b in blocks_not_to_format]
    scene_blocks_n = [b for b in scene_blocks_n if b not in blocks_not_to_format]
    scene_blocks_n = blocks_not_to_format+scene_blocks_n
    scene_blocks_n_names = [b.world_name for b in scene_blocks_n]
    for connection in scene_connections:
        try:
            output_code_connections += str(scene_blocks_n_names.index(connection.src) + 1)
            output_code_connections += ","
            output_code_connections += str(scene_blocks_n_names.index(connection.dst) + 1)
            output_code_connections += ";"
        except:
            raise NameError(connection.src, connection.dst)

    for block_ in scene_blocks_n:
        if block_.world_name not in blocks_not_to_format_names:
            output_code_blocks += block_.final_look
        else:
            not_formatted_code += block_.final_look

    def calculate_grid_sizes(code, grid_type, extra=None):
        """
        code: input_blocks string
        grid_type: 
            'flat_square'
            'flat_ratio'
            'wall'
            'wall_ratio'
            'cube'
            'custom'
        extra:
            float for ratio
            list [xs, ys, zs] for custom
        """

        blocks = [b for b in code.split("?")[0].split(";") if b]
        N = len(blocks)

        if grid_type == 'flat_square':
            xs = math.ceil(math.sqrt(N))
            ys = 1
            zs = math.ceil(N / xs)
            return xs, ys, zs

        elif grid_type == 'flat_ratio':
            if extra is None:
                raise ValueError("flat_ratio requires a ratio")
            ratio = float(extra)
            xs = math.ceil(math.sqrt(N * ratio))
            ys = 1
            zs = math.ceil(N / xs)
            return xs, ys, zs

        elif grid_type == 'wall':
            xs = math.ceil(math.sqrt(N))
            ys = math.ceil(N / xs)
            zs = 1
            return xs, ys, zs

        elif grid_type == 'wall_ratio':
            if extra is None:
                raise ValueError("wall_ratio requires a ratio")
            ratio = float(extra)
            xs = math.ceil(math.sqrt(N / ratio))
            ys = math.ceil(N / xs)
            zs = 1
            return xs, ys, zs

        elif grid_type == 'cube':
            s = math.ceil(N ** (1/3))
            return s, s, s

        elif grid_type == 'custom': 
            
            return [int(s) for s in extra] 
 
        else:
            raise ValueError(f"Unknown grid_type: {grid_type}")

    def format_block(grid_sizes, code):
        xg = []
        yg = []
        zg = []
        for y in range(grid_sizes[1]):
            for z in range(grid_sizes[2]):
                for x in range(grid_sizes[0]):
                    xg.append('')
                zg.append(xg)
                xg = []
            yg.append(zg)
            zg = []

        grid = yg
        input_blocks = code
        blocks = input_blocks.split("?")[0].split(";")
        b_blocks = []
        for i, b in enumerate(blocks):
            b = b.split(",")
            index = b[0]
            x = b[2]
            y = b[3]
            z = b[4]
            params = []
            if len(b) > 5:
                params = b[5].split("+")
            b_blocks.append(block(index, x, y, z, params, str(i), True))

        connections = input_blocks.split("?")[1]
        xs = grid_sizes[0]
        ys = grid_sizes[1]
        zs = grid_sizes[2]
        for yy, y in enumerate(grid):
            for zz, z in enumerate(y):
                for xx, x in enumerate(z):
                    index = xx+zz*xs+yy*zs*xs
                    if index >= len(blocks):
                        continue
                    b_blocks[index].x = str(xx)
                    b_blocks[index].y = str(yy)
                    b_blocks[index].z = str(zz)
                    b_blocks[index].calculate_final_look()
        return "".join([b.final_look for b in b_blocks])[:-1]+"?"+connections+"??"
        
    """grid_type: 
            'flat_square'
            'flat_ratio'
            'wall'
            'wall_ratio'
            'cube'
            'custom'
        extra:
            float for ratio (for *_ratio)
            tuple (x, y, z) for custom
          """
    grid_type = conf["grid_type"]+conf["extra"]
    if len(grid_type.split()) > 1:
        grid_sizes = calculate_grid_sizes(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??", grid_type.split()[0], grid_type.split()[1:len(grid_type.split())] )
    else:
        grid_sizes = calculate_grid_sizes(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??", grid_type.split()[0] )
    blocks = not_formatted_code+format_block(grid_sizes, output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")
    copy_or_print = conf["CopyOrPrint"]
    if copy_or_print == "print":
        print(blocks)
    else:
        pyperclip.copy(blocks)


def always_relay_on(block_to_relay_on, d_ff, output_block):
    """
    makes a d flip flop relay on some block like clock etc.
    """
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
def logic(start_pos: list[int], end_pos: list[int], width: int, block_type: int, fixed: bool = None):
    """
    generation of busses
    """
    global logics
    step = [(end_pos[i] - start_pos[i]) // max(1, width-1) for i in range(3)]
    blocks = []

    for b in range(width):
        pos = [start_pos[i] + step[i]*b for i in range(3)]
        blocks.append(block(block_type, pos[0], pos[1], pos[2], [], f"logic_{b}_{logics}", no_formatting=fixed))

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
    global mux_i_count
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
    return {"select": select, "output_logic": output_logic}

mux_c_count = 0
def mux_c(inputs: list, inputs_width: int, position: list[int]):
    global mux_c_count
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
            if bit == "1":
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
    return {"select": select, "output_logic": output_logic}

def connect_logic(logic_a: logic, logic_b: logic, order: int):
    """
    order: 1 for normal connection, -1 for reversed connection
    """

    if order == 1:
        for i, block_a in enumerate(logic_a):
            try:
                scene_connections.append(scene_connection(block_a.world_name, logic_b[i].world_name))
            except IndexError:
                raise IndexError("Not matching logic widths")
    elif order == -1:
        for i, block_a in enumerate(logic_a):
            try:
                scene_connections.append(scene_connection(block_a.world_name, logic_b[len(logic_b)-i-1].world_name))
            except IndexError:
                raise IndexError("Not matching logic widths")

def connect_adder(adder, logic_a, logic_b, logic_c):
    """
    connects buses with adder
    """
    A = [b for b in adder if b.world_name.startswith("r_adder_A_")]
    B = [b for b in adder if b.world_name.startswith("r_adder_B_")]
    C = [b for b in adder if b.world_name.startswith("r_adder_C_")]

    for i, b in enumerate(logic_a):
        scene_connections.append(scene_connection(b.world_name, A[i].world_name))
    for i, b in enumerate(logic_b):
        scene_connections.append(scene_connection(b.world_name, B[i].world_name))
    for i, b in enumerate(logic_c):
        scene_connections.append(scene_connection(C[i].world_name, b.world_name))

def connect_mux(mux, select_logic, output_logic):
    sel = mux["select"]
    output = mux["output_logic"]

    for i, b in enumerate(select_logic):
        scene_connections.append(scene_connection(b.world_name, sel[i].world_name))
    for i, b in enumerate(output):
        scene_connections.append(scene_connection(output_logic[i].world_name, b.world_name,))

const_num_count = 0
def const_num(num: int, pos: list[int], width: int):
    global const_num_count
    blocks = []
    num = bin(num)[2:].zfill(width)
    x = pos[0]
    y = pos[1]
    z = pos[2]

    for n in num:
        if n == "0":
            blocks.append(block(15, x, y, z, [], f"const_num_{x}_{const_num_count}"))
        else:
            blocks.append(block(0, x, y, z, [], f"const_num_{x}_{const_num_count}"))
        x += 1
    return blocks

comparator_count = 0
def comparator(input1: list[block], input2: list[block], width: int, pos: list[int]):
    global comparator_count, scene_connections
    y = pos[1]
    z = pos[2]
    Bigger = block(15, width, y, z, [], f"cmp_bigger_{comparator_count}")
    Less = block(15, width, y, z+1, [], f"cmp_less_{comparator_count}")
    Equal = block(1, width, y, z+2, [], f"cmp_equal_{comparator_count}")
    for bit in range(width):
        A = input1[bit]
        B = input2[bit]
        x = pos[0]+bit

        And1 = block(1, x, y, z, [], f"cmp_and1_{bit}_{comparator_count}")
        And2 = block(1, x, y, z+1, [], f"cmp_and2_{bit}_{comparator_count}")

        Xor = block(3, x, y, z+2, [], f"cmp_xor_{bit}_{comparator_count}")
        Nxor = block(0, x, y, z+3, [], f"cmp_nxor_{bit}_{comparator_count}")

        C = block(15, x, y, z+4, [], f"cmp_c_{bit}_{comparator_count}")

        Xnor = block(11, x, y, z+5, [], f"cmp_nb_{bit}_{comparator_count}")


        scene_connections.append(scene_connection(A.world_name, Xor.world_name))
        scene_connections.append(scene_connection(B.world_name, Xor.world_name))
        scene_connections.append(scene_connection(A.world_name, And1.world_name))
        scene_connections.append(scene_connection(B.world_name, And2.world_name))
        scene_connections.append(scene_connection(A.world_name, Xnor.world_name))
        scene_connections.append(scene_connection(B.world_name, Xnor.world_name))
        scene_connections.append(scene_connection(C.world_name, And1.world_name))
        scene_connections.append(scene_connection(C.world_name, And2.world_name))
        scene_connections.append(scene_connection(Xor.world_name, Nxor.world_name))
        scene_connections.append(scene_connection(Xnor.world_name, Equal.world_name))
        scene_connections.append(scene_connection(And1.world_name, Bigger.world_name))
        scene_connections.append(scene_connection(And2.world_name, Less.world_name))
        for c in range(width-bit-1):
            scene_connections.append(scene_connection(Nxor.world_name, f"cmp_c_{bit+c+1}"))
    return Bigger, Equal, Less
############################################################################################################



############################################################################################################


f = input("format? - y/n: ").lower()
if f == "y":
    build_scene()
elif f == "n":
    build_scene_no_formatting()
