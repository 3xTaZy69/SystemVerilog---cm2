class AND:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class OR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class NOT:
    def __init__(self, right):
        self.right = right

class XOR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class INPUT:
    def __init__(self, name, block_):
        self.name = name
        self.block = block_

class OUTPUT:
    def __init__(self, name, block_):
        self.name = name
        self.block = block_

class EQUAL:
    def __init__(self, dst, value):
        self.dst = dst
        self.value = value

class EQUALFF:
    def __init__(self, dst, value):
        self.dst = dst
        self.value = value

class MODULE:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

class LOGIC:
    def __init__(self, blocks):
        self.blocks = blocks

class ADD:
    def __init__(self, left, right, type='ripple'):
        self.left = left
        self.right = right
        self.type = type

class SUB:
    def __init__(self, left, right, type='ripple'):
        self.left = left
        self.right = right
        self.type = type
