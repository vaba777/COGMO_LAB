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
        #  print("Perceptual:", preceptual_type, "Cognitive:", cognitive_type, "Motor:", motor_type, "Total:", total_time, "ms")
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

def example3(
    perceptual_type="middle", cognitive_type="middle", motor_type="middle"):
  total_time = (
    start()
    + perceptualstep(perceptual_type)
    + perceptualstep(perceptual_type)
    + cognitivestep(cognitive_type)
    + cognitivestep(cognitive_type)
    + motorstep(motor_type)
  )
  return total_time

def example4(
    perceptual_type="middle", cognitive_type="middle", motor_type="middle"):
  second_stimulus_timings = [40, 80, 110, 150, 210, 240]
  results = []
  perceptual_time = perceptualstep(perceptual_type)
  cognitive_time = cognitivestep(cognitive_type)
  motor_time = motorstep(motor_type)
  for second_stimulus_time in second_stimulus_timings:
    first_perceptual_finished = perceptual_time
    second_perceptual_starts = max(
      second_stimulus_time, first_perceptual_finished
    )

    total_time = (
      second_perceptual_starts
      + perceptual_time
      + cognitive_time
      + cognitive_time
      + motor_time
    )
    results.append((second_stimulus_time, total_time))
  return results


print("Example 3:", example3())
print("Example 3 all fast:", example3("fast", "fast", "fast"))  
print("Example 3 fast perception, middle cognition, slow motor:", example3("fast", "middle", "slow") )

print("Example 4 all fast:", example4("fast", "fast", "fast"))
print("Example 4 all middle:", example4())
print("Example 4 all slow:", example4("slow", "slow", "slow"))

slow_results = example4("slow", "slow", "slow")
slowest_time = max(total_time for stimulus_time, total_time in slow_results)

print("Slowest predicted time:", slowest_time)

def error_factor(step_type):
  if step_type == "fast":
    return 3
  elif step_type == "middle":
    return 2
  elif step_type == "slow":
    return 0.5

def example5():
  types =  ["fast", "middle", "slow"]
  results = []
  trial_times = []
  error_percentages = []
  for perceptual_type in types:
    for cognitive_type in types:
      for motor_type in types:
        total_time = (
          start()
          + perceptualstep(perceptual_type)
          + perceptualstep(perceptual_type)
          + cognitivestep(cognitive_type)
          + cognitivestep(cognitive_type)
          + motorstep(motor_type)
        )
        error_probability = 0.01
        error_probability*= error_factor(perceptual_type)
        error_probability*= error_factor(perceptual_type)
        error_probability*= error_factor(cognitive_type)
        error_probability*= error_factor(cognitive_type)
        error_probability*= error_factor(motor_type)

        error_probability = min(error_probability, 1.0)
        error_percentage = error_probability * 100

        results.append(
                    (
                        perceptual_type,
                        cognitive_type,
                        motor_type,
                        total_time,
                        error_percentage
                    )
                )
        trial_times.append(total_time)
        error_percentages.append(error_percentage)

        print(
                    "Perceptual:", perceptual_type,
                    "Cognitive:", cognitive_type,
                    "Motor:", motor_type,
                    "Time:", total_time, "ms",
                    "Error:", error_percentage, "%"
                )
      plt.figure(figsize=(7, 5))
      plt.scatter(
      trial_times,
      error_percentages,
      alpha=0.7
  )
      plt.xlabel("Trial time (ms)")
  plt.ylabel("Error probability (%)")
  plt.title("Relationship between trial time and error probability")

  plt.ylim(0, 105)
  plt.grid(True, alpha=0.3)
  plt.tight_layout()

  plt.savefig("example5_scatterplot.png", dpi=300)
  plt.close()

  print("Number of combinations:", len(results))
  print("Scatterplot saved as example5_scatterplot.png")
  return results

example5()