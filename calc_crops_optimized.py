from scipy.stats import binom
from multiprocessing import Pool


class Crop:
    name: str
    growth_chance = float
    growth_steps = int

    def __init__(self, name, growth_chance, growth_steps):
        self.name = name
        self.growth_chance = growth_chance
        self.growth_steps = growth_steps

    def get(self):
        return (self.growth_chance, self.growth_steps)


# Amount of ticks per second in the area. Can be lower if the server is lagging or higher when using certain mods.
TICK_RATE = 20

# Starting point. Unless your crop grows extremely quickly, there is no way to get under this.
START = 10000

# Amount of ticks each step of the calculation "skips". Lower number gives higher precision.
STEP = 100

# Target chance (in %) for your crops to have fully grown.
TARGET = 99
TARGET_PROBABILITY = TARGET / 100

# Put the current "RandomTickSpeed" gamerule current number. If this is higher, your crops will grow faster. THey will grow slower for lower numbers.
RANDOM_TICK_SPEED = 3
RANDOM_TICK_CHANCE = RANDOM_TICK_SPEED / (16 * 16 * 16)

# List of Crops. Following the format: name, growth chance on random tick, amount of growth steps.
CROPS = [Crop("Wheat", 14.29, 7),
         Crop("Carrot", 14.29, 7),
         Crop("Potato", 14.29, 7),
         Crop("Pumpkin", 20, 4),
         Crop("Sugar Cane", 100, 16 * 2),
         Crop("Melon", 20, 4),
         Crop("Cactus", 100, 16 * 2),
         Crop("Cocoa Beans", 20, 3),
         Crop("Mushroom", 4, 1),
         Crop("Nether Wart", 10, 3)]


def MagicProbabilityCalculator(prob_growth, growth_qt, tries):
    ret = 0
    tmp = 0
    for i in range(0, growth_qt):
        tmp = binom.pmf(i, tries, prob_growth)
        ret += tmp
        del tmp
    return ret


def process_crop(current: Crop):
    randomtick_growth_chance, crop_growth_num = current.get()
    crop_pro = randomtick_growth_chance / 100 * RANDOM_TICK_CHANCE
    n = START
    while (MagicProbabilityCalculator(crop_pro, crop_growth_num, n) >= 1 - TARGET_PROBABILITY):
        n += STEP
    print(f"{current.name:<10} \t {n} ticks\t{n / TICK_RATE} sec\t {n / TICK_RATE / 60:.2f} min")


if __name__ == "__main__":
    processes = Pool(len(CROPS))
    processes.map(process_crop, CROPS)
    processes.close()
    processes.join()
