import math

def get_primes_oldest(input_list):
    result_list = list()
    for element in input_list:
        if is_prime(element):
            result_list.append()

    return result_list

# or better yet...

def get_primes_old(input_list):
    return (element for element in input_list if is_prime(element))

# Yield example 1
def get_primes(number):
    while True:
        if is_prime(number):
            yield number
        number += 1

# not germane to the example, but here's a possible implementation of
# is_prime...

def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0: 
                return False
        return True
    return False

#for prime in get_primes(1):
#    print prime


def simple():
    yield 1
    yield 2
    yield 3
    yield 4

def use_simple():
  s = simple()
  print next(s)
  print next(s)
  print next(s)
  print next(s)
  print next(s)

#use_simple()

# Yield example 2.
def get_primes(number):
    while True:
        if is_prime(number):
            number = yield number
        number += 1

def print_successive_primes(iterations, base=10):
    prime_generator = get_primes(base)
    prime_generator.send(None)
    for power in range(iterations):
        print(prime_generator.send(base ** power))

def print_my_primes():
    gen = get_primes(10)
    print next(gen)
    #gen.send(None)
    print gen.send(200)
    gen = get_primes(400)
    print next(gen)
    #print next(gen)

print_my_primes()
#print_successive_primes(4)