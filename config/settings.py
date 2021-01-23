# ========================= Mutation probabilities ========================== #
MUT_ADD_LINK = 0.05
MUT_WEIGHT_SHIFT = 0.05
MUT_WEIGHT_REASSIGN = 0.05
MUT_ADD_NODE = 0.05
MUT_TOGGLE_LINK = 0.05

# ======================== Initial network topology ========================= #
INPUT_NODES = 2
OUTPUT_NODES = 1
BIAS_NODES = 1  # Recommended to leave this unchanged
OUT_NODE_X = 0.9
IN_NODE_X = 0.1
BIAS_NODE_X = 0.01
WEIGHT_INITIAL_CAP = 4.0

# ========================== Population parameters ========================== #
POPULATION_SIZE = 1000
EXCESS_COEFFICIENT = 2.0
DISJOINT_COEFFICIENT = 2.0
WEIGHT_COEFFICIENT = 1.0
DELTA_THRESHOLD = 3.5
SURVIVORS = 0.6  # MUST be above 0.5!

# ========================= General configurations ========================== #
RESOLUTION = [720, 480]
BG_COLOR = 247, 235, 203
