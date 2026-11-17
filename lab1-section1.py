import matplotlib.pyplot as plt

def start(type="middle"):
  return 0

def perceptualstep(type="middle"):
  if type=="fast":
    return 50
  elif type=="middle":
    return 100
  elif type=="slow":
    return 200
  else:
    raise ValueError("Invalid type. Type 'fast', 'middle', or 'slow'.") 

def cognitivestep(type="middle"):
  if type=="fast":
    return 25
  elif type=="middle":
    return 70
  elif type=="slow":
    return 170
  else:
    raise ValueError("Invalid type. Type 'fast', 'middle', or 'slow'.") 

def motorstep(type="middle"):
  if type=="fast":
    return 30
  elif type=="middle":
    return 70
  elif type=="slow":
    return 100
  else:
    raise ValueError("Invalid type. Type 'fast', 'middle', or 'slow'.") 

def example1():
  total_time = (
    start()
    + perceptualstep()
    + cognitivestep()
    + motorstep()
  )
  return total_time 

def example2(completeness="extremes"):
  if completeness=="extremes":
    fast_time = (
      start()
      + perceptualstep("fast")
      + cognitivestep("fast")
      + motorstep("fast")
    )

    middle_time = (
    start()
    + perceptualstep("middle")
    + cognitivestep("middle")
    + motorstep("middle")
   )

    slow_time = (
    start()
    + perceptualstep("slow")
    + cognitivestep("slow")
    + motorstep("slow")
   )
    return [fast_time, middle_time, slow_time]
 

  elif completeness == "all":
    types = ["fast", "middle", "slow"]
    all_times = []
    for preceptual_type in types:
      for cognitive_type in types:
        for motor_type in types:
          total_time = (
            start()
            + perceptualstep(preceptual_type)
            + cognitivestep(cognitive_type)
            + motorstep(motor_type)
          )
          all_times.append(total_time)
          print("Perceptual:", preceptual_type, "Cognitive:", cognitive_type, "Motor:", motor_type, "Total:", total_time, "ms")
    print("Number of combinations:", len(all_times))
    plt.figure(figsize=(5,6))
    plt.boxplot(all_times)
    plt.ylabel("Time (ms)")
    plt.ylim(0, 500)
    plt.xticks([1], ["All combinations"])
    plt.title("All 27 processing combinations")
    plt.tight_layout()
    plt.savefig("example2_boxplot.png", dpi=300)
    plt.close()

    print("Boxplot saved as example2_boxplot.png")
    
    return all_times

  
  else:
   raise ValueError("completeness must be extremes or all.")



print("Example 1:", example1())
print("Example 2:", example2())
example2("all")