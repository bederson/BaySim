import random


def gen_unique_rand(max, rands):
    have_num = False
    while not have_num:
        num = random.randint(1, max)
        have_num = not num in rands
    return num


def unique_rands(num_rands, max):
    rands = []
    for i in range(num_rands):
        num = gen_unique_rand(max, rands)
        rands.append(num)
    return rands