
def dir_gen():
    dirs = [(0, -1), (1, 0), (0, 1), (0, 1), (-1, 0)]
    while True:
        for dire in dirs:
            yield dire


def pos_gen():
    steer = dir_gen()
    level = 0
    currpos = (0, 0)
    side = 1
    # print("currpos=%s, direz=%s, level=%d, side=%d" % (str(currpos), "none", level, side))
    yield currpos
    while True:
        direc = next(steer)
        currpos = (currpos[0] + direc[0], currpos[1] + direc[1])
        # print("currpos=%s, direz=%s, level=%d, side=%d" % (str(currpos), str(direc), level, side))
        yield currpos
        if side % 4 == 0:
            level += 1
            direc = next(steer)
        for xtra in range((level * 3)):
            currpos = (currpos[0] + direc[0], currpos[1] + direc[1])
            # print("currpos=%s, direz=%s, level=%d, side=%d" % (str(currpos), str(direc), level, side))
            yield currpos
        side += 1


def walk_spiral(steps, normalize=False):
    walker = pos_gen()
    walked = []
    for step in range(steps):
        walked.append(next(walker))
    if normalize:
        minx = min(map(lambda pair: pair[0], walked))
        miny = min(map(lambda pair: pair[1], walked))
        walked = list(map(lambda pair: (pair[0] - minx, pair[1] - miny), walked))
    return walked


def draw_spiral(symbols):
    steps = walk_spiral(len(symbols), normalize=True)
    width = max(map(lambda pair: pair[0], steps))+1
    height = max(map(lambda pair: pair[1], steps))+1
    grid = [["  " for _ in range(width)] for _ in range(height)]
    for step in steps:
        (x, y) = step
        grid[y][x] = symbols.pop(0)
    return grid


def pretty_print_grid(grid, title, footer):
    width = len(grid[0]) * 2
    formatted_title = "[ %s ]" % title
    formatted_footer = "[ %s ]" % footer
    buff = "+%s+\n" % formatted_title.center(width, "-")
    for line in grid:
        buff += "|"
        for cell in line:
            buff += cell
        buff += "|\n"
    buff += "+%s+" % formatted_footer.center(width, "-")
    return buff


def debug_print_grid(grid):
    for line in grid:
        for cell in line:
            print(cell, end="")
        print()
