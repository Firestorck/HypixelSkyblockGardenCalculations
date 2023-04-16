from scipy.stats import binom


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


def MagicProbabilityCalculator(prob_growth, growth_qt, tries):
    ret = 0
    tmp = 0
    for i in range(0, growth_qt):
        tmp = binom.pmf(i, tries, prob_growth)
        ret += tmp
        del tmp
    return ret


if __name__ == "__main__":
    start = 10000
    step = 10
    limit = 0.99
    random_tick_speed = 3
    crops = [Crop("Wheat", 14.29, 7),
             Crop("Carrot", 14.29, 7),
             Crop("Potato", 14.29, 7),
             Crop("Pumpkin", 20, 4),
             Crop("Sugar Cane", 100, 16 * 2),
             Crop("Melon", 20, 4),
             Crop("Cactus", 100, 16 * 2),
             Crop("Cocoa Beans", 20, 3),
             Crop("Mushroom", 4, 1),
             Crop("Nether Wart", 10, 3)]

    for current in crops:
        randomtick_growth_chance, crop_growth_num = current.get()
        crop_pro = randomtick_growth_chance / 100 * (random_tick_speed / (16 * 16 * 16))
        n = start
        while (MagicProbabilityCalculator(crop_pro, crop_growth_num, n) >= 1 - limit):
            n += step
        print(f"{current.name:<10} \t {n} ticks\t{n / 20} sec\t {n / 20 / 60:.2f} min")
