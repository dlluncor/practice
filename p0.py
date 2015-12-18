
def join(path, *paths):
  p = [path]
  for part in paths:
    p.append(part)
  print p

def main():
  join('yo', 'mang', 'whatsup')

main()
