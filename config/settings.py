# ========================= Mutation probabilities ========================== #
MUTATION_RATE = 0.25
MUT_ADD_LINK = 0.05
MUT_WEIGHT_ADJUST = 0.8  # Controls how likely the next two mutations are to occur
MUT_WEIGHT_SHIFT = 0.9
MUT_WEIGHT_REASSIGN = 0.1
MUT_ADD_NODE = 0.03
MUT_TOGGLE_LINK = 0  # Experimental - not safe to enable yet

# ======================== Initial network topology ========================= #
INPUT_NODES = 2
OUTPUT_NODES = 1
BIAS_NODES = 1  # Recommended to leave this unchanged
OUT_NODE_X = 0.9
IN_NODE_X = 0.1
WEIGHT_INITIAL_CAP = 3.0

# ========================== Population parameters ========================== #
POPULATION_SIZE = 150
EXCESS_COEFFICIENT = 1.0
DISJOINT_COEFFICIENT = 1.0
WEIGHT_COEFFICIENT = 0.4
DELTA_THRESHOLD = 3.0
SURVIVORS = 0.2

# ========================= General configurations ========================== #
RESOLUTION = [720, 480]
BG_COLOR = 247, 235, 203
