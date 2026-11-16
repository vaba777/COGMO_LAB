def start():
  return 0

def perceptualstep():
  return 100 

def cognitivestep():
  return 70

def motorstep():
  return 70

def example1():
  total_time = (
    start()
    + perceptualstep()
    + cognitivestep()
    + motorstep()
  )
  return total_time 

print(example1())
