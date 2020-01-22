import random
import string


def str_random(length=8):

    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
