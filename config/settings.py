# =========================== Mutation properties ============================ #
MUTATION_RATE = 0.35  # Portion of individuals to reproduce asexually through mutation

# Once an individual is chosen to mutate, they will mutate up to this many times, choosing
# from the mutations below (and respecting the assigned probabilities)
MUTATIONS_AT_ONCE = 10

MUT_ADD_LINK = 0.18
MUT_ADD_NODE = 0.01
MUT_TOGGLE_LINK = 0.01

MUT_WEIGHT_ADJUST = 0.8  # Controls overall how likely the next two mutation types are to occur
MUT_WEIGHT_SHIFT = 0.9
MUT_WEIGHT_REASSIGN = 0.1

# ======================== Initial network topology ========================= #
INPUT_NODES = 2
OUTPUT_NODES = 1
BIAS_NODES = 1  # Recommended to leave this unchanged
IN_NODE_X = 0.1
OUT_NODE_X = 0.9
WEIGHT_INITIAL_CAP = 4.0

# ========================== Population parameters ========================== #
POPULATION_SIZE = 150
EXCESS_COEFFICIENT = 2.0
DISJOINT_COEFFICIENT = 2.0
WEIGHT_COEFFICIENT = 1.0
DELTA_THRESHOLD = 3.0
SURVIVORS = 0.2
ELITES = 0.1

# ========================= General configurations ========================== #
RESOLUTION = [720, 480]
BG_COLOR = 247, 235, 203
