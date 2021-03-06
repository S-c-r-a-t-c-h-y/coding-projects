class Lantern:
    def __init__(self, lanterns_list: list, timer: int):
        self.lantern_list = lanterns_list
        self.timer = timer
        lanterns_list.append(self)

    def set_list(self, new_list):
        self.lantern_list = new_list

    def count_down(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            self.lantern_list.append(Lantern(self.lantern_list, 8))


initial_state = [
    5,
    1,
    1,
    3,
    1,
    1,
    5,
    1,
    2,
    1,
    5,
    2,
    5,
    1,
    1,
    1,
    4,
    1,
    1,
    5,
    1,
    1,
    4,
    1,
    1,
    1,
    3,
    5,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    4,
    4,
    4,
    1,
    1,
    1,
    1,
    1,
    4,
    1,
    1,
    1,
    1,
    1,
    5,
    1,
    1,
    1,
    4,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    4,
    1,
    4,
    1,
    1,
    2,
    3,
    1,
    1,
    1,
    1,
    4,
    1,
    2,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    4,
    4,
    1,
    4,
    2,
    1,
    1,
    1,
    1,
    1,
    4,
    3,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    1,
    3,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    3,
    1,
    3,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    2,
    3,
    1,
    2,
    1,
    1,
    4,
    1,
    1,
    5,
    3,
    1,
    1,
    1,
    2,
    4,
    1,
    1,
    2,
    4,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    4,
    3,
    1,
    2,
    1,
    2,
    1,
    5,
    1,
    2,
    1,
    1,
    5,
    1,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    4,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    5,
    1,
    1,
    1,
    1,
    5,
    1,
    4,
    1,
    1,
    1,
    4,
    1,
    3,
    4,
    1,
    4,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    5,
    1,
    3,
    1,
    1,
    1,
    1,
    4,
    1,
    5,
    3,
    1,
    1,
    1,
    1,
    1,
    5,
    1,
    1,
    1,
    2,
    2,
]

l = []
for timer in initial_state:
    Lantern(l, timer)

for i in range(80):
    for lantern in l.copy():
        lantern.count_down()

    print(i, len(l))

275070380
