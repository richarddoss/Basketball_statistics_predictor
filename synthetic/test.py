from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import statGeneration as s
playerRatingTrue,minutesPlayedTrue=s.generateTrueStrength()
s.statsGenerate(playerRatingTrue,minutesPlayedTrue)