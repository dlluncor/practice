

def f(x):
  if x == 1:
    return 1
  return 2 * f(x - 1) + x * x

def main():
  inputs = [1, 2, 3, 4, 5]
  for i in inputs:
    print('f(%d) = %d' % (i, f(i)))

main()
