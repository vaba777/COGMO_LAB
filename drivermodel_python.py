### 
### This code is developed by Christian P. Janssen of Utrecht University
### It is intended for students from the Master's course Cognitive Modeling
### Large parts are based on the following research papers:
### Janssen, C. P., & Brumby, D. P. (2010). Strategic adaptation to performance objectives in a dual‐task setting. Cognitive science, 34(8), 1548-1560. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1551-6709.2010.01124.x
### Janssen, C. P., Brumby, D. P., & Garnett, R. (2012). Natural break points: The influence of priorities and cognitive and motor cues on dual-task interleaving. Journal of Cognitive Engineering and Decision Making, 6(1), 5-29. https://journals.sagepub.com/doi/abs/10.1177/1555343411432339
###
### If you want to use this code for anything outside of its intended purposes (training of AI students at Utrecht University), please contact the author:
### c.p.janssen@uu.nl



### 
### import packages
###

import numpy
import matplotlib.pyplot as plt

###
###
### Global parameters. These can be called within functions to change (Python: make sure to call GLOBAL)
###
###


###
### Car / driving related parameters
###
steeringUpdateTime = 250    #in ms ## How long does one steering update take? (250 ms consistent with Salvucci 2005 Cognitive Science)
timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
startingPositionInLane = 0.27 			#assume that car starts already slightly away from lane centre (in meters) (cf. Janssen & Brumby, 2010)


#parameters for deviations in car drift due the simulator environment: See Janssen & Brumby (2010) page 1555
gaussDeviateMean = 0
gaussDeviateSD = 0.13 ##in meter/sec



### The car is controlled using a steering wheel that has a maximum angle. Therefore, there is also a maximum to the lateral velocity coming from a steering update
maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
minLateralVelocity = -1* maxLateralVelocity

startvelocity = 0 	#a global parameter used to store the lateral velocity of the car


###
### Switch related parameters
###
retrievalTimeWord = 200   #ms. ## How long does it take to think of the next word when interleaving after a word (time not spent driving, but drifting)
retrievalTimeSentence = 300 #ms. ## how long does it take to retrieve a sentence from memory (time not spent driving, but drifting)



###
### parameters for typing task
###
timePerWord = 0  ### ms ## How much time does one word take
wordsPerMinuteMean = 39.33   # parameters that control typing speed: when typing two fingers, on average you type this many words per minute. From Jiang et al. (2020; CHI)
wordsPerMinuteSD = 10.3 ## this si standard deviation (Jiang et al, 2020)


## Function to reset all parameters. Call this function at the start of each simulated trial. Make sure to reset GLOBAL parameters.
def resetParameters():
    global timePerWord
    global retrievalTimeWord
    global retrievalTimeSentence 
    global steeringUpdateTime 
    global startingPositionInLane 
    global gaussDeviateMean
    global gaussDeviateSD 
    global gaussDriveNoiseMean 
    global gaussDriveNoiseSD 
    global timeStepPerDriftUpdate 
    global maxLateralVelocity 
    global minLateralVelocity 
    global startvelocity
    global wordsPerMinuteMean
    global wordsPerMinuteSD
    
    timePerWord = 0  ### ms

    retrievalTimeWord = 200   #ms
    retrievalTimeSentence = 300 #ms
    
    steeringUpdateTime = 250    #in ms
    startingPositionInLane = 0.27 			#assume that car starts already away from lane centre (in meters)
    

    gaussDeviateMean = 0
    gaussDeviateSD = 0.13 ##in meter/sec
    gaussDriveNoiseMean = 0
    gaussDriveNoiseSD = 0.1	#in meter/sec
    timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
    maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
    minLateralVelocity = -1* maxLateralVelocity
    startvelocity = 0 	#a global parameter used to store the lateral velocity of the car
    wordsPerMinuteMean = 39.33
    wordsPerMinuteSD = 10.3

    



##calculates if the car is not accelerating (m/s) more than it should (maxLateralVelocity) or less than it should (minLateralVelocity)  (done for a vector of numbers)
def velocityCheckForVectors(velocityVectors):
    global maxLateralVelocity
    global minLateralVelocity

    velocityVectorsLoc = velocityVectors

    if (type(velocityVectorsLoc) is list):
            ### this can be done faster with for example numpy functions
        velocityVectorsLoc = velocityVectors
        for i in range(len(velocityVectorsLoc)):
            if(velocityVectorsLoc[i]>1.7):
                velocityVectorsLoc[i] = 1.7
            elif (velocityVectorsLoc[i] < -1.7):
                velocityVectorsLoc[i] = -1.7
    else:
        if(velocityVectorsLoc > 1.7):
            velocityVectorsLoc = 1.7
        elif (velocityVectorsLoc < -1.7):
            velocityVectorsLoc = -1.7

    return velocityVectorsLoc  ### in m/s
    




## Function to determine lateral velocity (controlled with steering wheel) based on where car is currently positioned. See Janssen & Brumby (2010) for more detailed explanation.
## Lateral velocity update depends on current position in lane. Intuition behind function: the further away you are, the stronger the correction will be that a human makes
def vehicleUpdateActiveSteering(LD):

    latVel = 0.2617 * LD*LD + 0.0233 * LD - 0.022
    returnValue = velocityCheckForVectors(latVel)
    return returnValue ### in m/s
    



### function to update lateral deviation in cases where the driver is NOT steering actively (when they are distracted by typing for example). Draw a value from a random distribution. This can be added to the position where the car is already.
def vehicleUpdateNotSteering():
    
    global gaussDeviateMean
    global gaussDeviateSD 

    

    vals = numpy.random.normal(loc=gaussDeviateMean, scale=gaussDeviateSD,size=1)[0]
    returnValue = velocityCheckForVectors(vals)
    return returnValue   ### in m/s





### Function to run a trial. Needs to be defined by students (section 2 and 3 of assignment)

def runTrial(nrWordsPerSentence =5,nrSentences=3,nrSteeringMovementsWhenSteering=2, interleaving="word",runNumber=None,makePlot=True): 
     global timePerWord
     locPos = []
     locColor = []
     trialTime = 0	
     startingPositionInLane = 0.27
     currentPosition = startingPositionInLane
     locPos.append(currentPosition)
     locColor.append("blue")
     typingSpeedWPM = numpy.random.normal(
        loc=wordsPerMinuteMean,
        scale=wordsPerMinuteSD
     )

     timePerWord = 60000 / typingSpeedWPM


     print("Typing speed:", round(typingSpeedWPM, 2), "WPM")
     print("Time per word:", round(timePerWord, 2), "ms")

     if interleaving in ("word", "threeWords"):
            print("Running", interleaving, "strategy")
            wordsBeforeSteering = 1 if interleaving == "word" else 3
            for sentenceIndex in range(nrSentences):
                print("Starting sentence:", sentenceIndex + 1)
                for wordIndex in range(nrWordsPerSentence):
                    wordDuration = timePerWord + retrievalTimeWord
                    if wordIndex == 0:
                        wordDuration += retrievalTimeSentence
                    numberOfDriftUpdates = int(
                        wordDuration // timeStepPerDriftUpdate
                    )

                    for driftIndex in range(numberOfDriftUpdates):
                        driftVelocity = vehicleUpdateNotSteering()

                        driftDistance = driftVelocity * (
                            timeStepPerDriftUpdate / 1000
                        )

                        currentPosition += driftDistance
                        locPos.append(currentPosition)
                        locColor.append("red")

                    isLastWord = (
                    sentenceIndex == nrSentences - 1
                    and wordIndex == nrWordsPerSentence - 1
                    )
                    reachedBreakPoint = (
                        (wordIndex + 1) % wordsBeforeSteering == 0
                        or wordIndex == nrWordsPerSentence - 1
                    )

                    if reachedBreakPoint and not isLastWord:
                            for steeringIndex in range(
                                nrSteeringMovementsWhenSteering
                                ):
                                steeringSpeed = abs(
                                    vehicleUpdateActiveSteering(
                                        abs(currentPosition)
                                    )
                                )
                                if currentPosition > 0:
                                    steeringVelocity = -steeringSpeed
                                elif currentPosition < 0:
                                    steeringVelocity = steeringSpeed
                                else:
                                    steeringVelocity = 0
                                numberOfSteeringUpdates = int(
                                    steeringUpdateTime
                                    // timeStepPerDriftUpdate
                                )

                                for updateIndex in range(
                                    numberOfSteeringUpdates
                                ):
                                    steeringDistance = steeringVelocity * (
                                        timeStepPerDriftUpdate / 1000
                                    )

                                    currentPosition += steeringDistance

                                    locPos.append(currentPosition)
                                    locColor.append("blue")
                                trialTime += steeringUpdateTime
                        

                


                    trialTime += wordDuration

                    
                print(
                    "Sentence:", sentenceIndex + 1,
                    "Word:", wordIndex + 1,
                    "Duration:", round(wordDuration, 2), "ms",
                    "Current time:", round(trialTime, 2), "ms"
                )
     elif interleaving == "sentence":
        print("Running sentence strategy")

        for sentenceIndex in range(nrSentences):
            print("Starting sentence:", sentenceIndex + 1)

            
            for wordIndex in range(nrWordsPerSentence):
                
                wordDuration = timePerWord

                
                if wordIndex == 0:
                    wordDuration += retrievalTimeSentence

                
                numberOfDriftUpdates = int(
                    wordDuration // timeStepPerDriftUpdate
                )

                for driftIndex in range(numberOfDriftUpdates):
                    driftVelocity = vehicleUpdateNotSteering()
                    driftDistance = driftVelocity * (
                        timeStepPerDriftUpdate / 1000
                    )

                    currentPosition += driftDistance
                    locPos.append(currentPosition)
                    locColor.append("red")

                trialTime += wordDuration

                print(
                    "Sentence:", sentenceIndex + 1,
                    "Word:", wordIndex + 1,
                    "Duration:", round(wordDuration, 2), "ms",
                    "Current time:", round(trialTime, 2), "ms"
                )

            
            isLastSentence = sentenceIndex == nrSentences - 1

            if not isLastSentence:
                for steeringIndex in range(
                    nrSteeringMovementsWhenSteering
                ):
                    steeringSpeed = abs(
                        vehicleUpdateActiveSteering(
                            abs(currentPosition)
                        )
                    )

                    
                    if currentPosition > 0:
                        steeringVelocity = -steeringSpeed
                    elif currentPosition < 0:
                        steeringVelocity = steeringSpeed
                    else:
                        steeringVelocity = 0

                    numberOfSteeringUpdates = int(
                        steeringUpdateTime
                        // timeStepPerDriftUpdate
                    )

                    for updateIndex in range(
                        numberOfSteeringUpdates
                    ):
                        steeringDistance = steeringVelocity * (
                            timeStepPerDriftUpdate / 1000
                        )

                        currentPosition += steeringDistance
                        locPos.append(currentPosition)
                        locColor.append("blue")

                    trialTime += steeringUpdateTime
     elif interleaving == "drivingOnly":
        print("Running driving-only baseline")

        
        
        
        totalTypingTime = (
            nrSentences * retrievalTimeSentence
            + nrSentences * nrWordsPerSentence * timePerWord
        )

        numberOfSteeringPeriods = int(
            totalTypingTime // steeringUpdateTime
        )

        
        for steeringIndex in range(numberOfSteeringPeriods):
            steeringSpeed = abs(
                vehicleUpdateActiveSteering(
                    abs(currentPosition)
                )
            )

            
            if currentPosition > 0:
                steeringVelocity = -steeringSpeed
            elif currentPosition < 0:
                steeringVelocity = steeringSpeed
            else:
                steeringVelocity = 0

            numberOfSteeringUpdates = int(
                steeringUpdateTime
                // timeStepPerDriftUpdate
            )

            for updateIndex in range(
                numberOfSteeringUpdates
            ):
                steeringDistance = steeringVelocity * (
                    timeStepPerDriftUpdate / 1000
                )

                currentPosition += steeringDistance
                locPos.append(currentPosition)
                locColor.append("blue")

        
        trialTime = totalTypingTime

     elif interleaving == "none":
        print("Running no-steering baseline")

        
        locColor[0] = "red"

        
        totalTypingTime = (
            nrSentences * retrievalTimeSentence
            + nrSentences
            * nrWordsPerSentence
            * timePerWord
        )

        numberOfDriftUpdates = int(
            totalTypingTime
            // timeStepPerDriftUpdate
        )

        
        for driftIndex in range(
            numberOfDriftUpdates
        ):
            driftVelocity = vehicleUpdateNotSteering()

            driftDistance = driftVelocity * (
                timeStepPerDriftUpdate / 1000
            )

            currentPosition += driftDistance
            locPos.append(currentPosition)
            locColor.append("red")

        trialTime = totalTypingTime

     print("Total typing time:", round(trialTime, 2), "ms")
     print("Number of stored positions:", len(locPos))
     print("Current lane position:", round(currentPosition, 4), "m")
     print("Final time:", trialTime)
     print("Final position:", currentPosition)
     print("Strategy:", interleaving)

     absolutePositions = [abs(position) for position in locPos]
     meanPosition = numpy.mean(absolutePositions)
     maxPosition = max(absolutePositions)

     if makePlot:

        timeValues = numpy.arange(len(locPos)) * timeStepPerDriftUpdate

        plt.figure(figsize=(10, 5))

        plt.scatter(
            timeValues,
            locPos,
            c=locColor,
            s=10
        )

        plt.axhline(
            y=0,
            color="black",
            linestyle="--",
            linewidth=1
        )

        plt.xlabel("Time (ms)")
        plt.ylabel("Lane position (m)")
        plt.title("Driving and typing - " + interleaving + " strategy")

        summaryText = (
            "Total trial time = "
            + str(round(trialTime, 2))
            + " ms\nMean absolute position = "
            + str(round(meanPosition, 4))
            + " m\nMax absolute position = "
            + str(round(maxPosition, 4))
            + " m"
        )

        plt.text(
            0.02,
            0.98,
            summaryText,
            transform=plt.gca().transAxes,
            verticalalignment="top",
            bbox=dict(
                boxstyle="round",
                facecolor="white",
                alpha=0.8
            )
        )

        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        
        if runNumber is None:
            plotFileName = f"{interleaving}_strategy_plot.png"
        else:
            plotFileName = (
            f"{interleaving}_strategy_plot_{runNumber:02d}.png"
        )
        plt.savefig(plotFileName, dpi=300)
        print("Plot saved as:", plotFileName)
        plt.close()

     print("Mean absolute position:", round(meanPosition, 4), "m")
     print("Max absolute position:", round(maxPosition, 4), "m")

     return (
        float(trialTime),
        float(meanPosition),
        float(maxPosition)
     )


     

     
     

     

    #  return trialTime, locPos, locColor

# runTrial(interleaving="sentence")
# for runNumber in range(1, 11):
#     print("\nRunning sentence trial:", runNumber)

#     runTrial(
#         nrWordsPerSentence=17,
#         nrSentences=10,
#         nrSteeringMovementsWhenSteering=4,
#         interleaving="sentence",
#         runNumber=runNumber
#     )
# for runNumber in range(1, 11):
#     print("\nRunning word trial:", runNumber)

#     runTrial(
#         nrWordsPerSentence=17,
#         nrSentences=10,
#         nrSteeringMovementsWhenSteering=4,
#         interleaving="word",
#         runNumber=runNumber
#     )
# runTrial(
#     nrWordsPerSentence=5,
#     nrSentences=3,
#     nrSteeringMovementsWhenSteering=2,
#     interleaving="drivingOnly"
# )
# runTrial(
#     nrWordsPerSentence=5,
#     nrSentences=3,
#     nrSteeringMovementsWhenSteering=2,
#     interleaving="none"    
# )
# result = runTrial(
#     nrWordsPerSentence=5,
#     nrSentences=3,
#     nrSteeringMovementsWhenSteering=2,
#     interleaving="threeWords",
#     makePlot=True
# )
# print("Returned results:",result)
    
    




### function to run multiple simulations. Needs to be defined by students (section 3 of assignment)
def runSimulations(nrSims=100):
    import io
    import contextlib
    import numpy as np

    strategies = ["none", "drivingOnly", "word", "sentence"]
    markers = {
        "none": "o",
        "drivingOnly": "s",
        "word": "^",
        "sentence": "D",
    }
    colors = {
        "none": "tab:red",
        "drivingOnly": "tab:green",
        "word": "tab:blue",
        "sentence": "tab:purple",
    }
    results = {strategy: [] for strategy in strategies}

    for strategy in strategies:
        print(f"\nRunning {nrSims} simulations for {strategy}...")
        for simNumber in range(1, nrSims + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                trialTime, meanPosition, maxPosition = runTrial(
                    nrWordsPerSentence=np.random.randint(15, 21),
                    nrSentences=10,
                    nrSteeringMovementsWhenSteering=4,
                    interleaving=strategy,
                    runNumber=simNumber,
                    makePlot=False,
                )
            results[strategy].append(
                (trialTime, maxPosition)
            )
        print("Finished", strategy)

    plt.figure(figsize=(10, 6))

    for strategy in strategies:
        trialTimes = np.array(
            [row[0] for row in results[strategy]]
        )
        maxPositions = np.array(
            [row[1] for row in results[strategy]]
        )

        # Individual simulations: grey points with a unique marker.
        plt.scatter(
            trialTimes,
            maxPositions,
            color="0.70",
            marker=markers[strategy],
            alpha=0.45,
            s=28,
        )

        # Condition mean with standard-deviation error bars.
        plt.errorbar(
            trialTimes.mean(),
            maxPositions.mean(),
            xerr=trialTimes.std(ddof=1),
            yerr=maxPositions.std(ddof=1),
            fmt=markers[strategy],
            color=colors[strategy],
            markeredgecolor="black",
            markersize=11,
            elinewidth=2,
            capsize=5,
            label=strategy,
        )

    plt.xlabel("Total trial time (ms)")
    plt.ylabel("Maximum lateral deviation (m)")
    plt.title(
        "Driving and typing performance across strategies"
    )
    plt.grid(alpha=0.25)
    plt.legend(title="Strategy")
    plt.tight_layout()
    plt.savefig(
        "section3A_simulation_plot.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()

    print(
        "\nSection 3A plot saved as: "
        "section3A_simulation_plot.png"
    )
    return results


def runBonusThreeWords(nrSims=100):
    import io
    import contextlib

    strategies = ["word", "threeWords", "sentence"]
    colors = {"word": "red", "threeWords": "purple", "sentence": "blue"}
    results = {strategy: [] for strategy in strategies}

    for strategy in strategies:
        for _ in range(nrSims):
            with contextlib.redirect_stdout(io.StringIO()):
                trialTime, _, maxPosition = runTrial(
                    nrWordsPerSentence=17,
                    nrSentences=10,
                    nrSteeringMovementsWhenSteering=4,
                    interleaving=strategy,
                    makePlot=False,
                )
            results[strategy].append((trialTime, maxPosition))

    plt.figure(figsize=(9, 5))
    for strategy in strategies:
        trialTimes = [row[0] / 1000 for row in results[strategy]]
        maxPositions = [row[1] for row in results[strategy]]
        plt.scatter(
            trialTimes,
            maxPositions,
            alpha=0.55,
            s=22,
            color=colors[strategy],
            label=strategy,
        )

    plt.xlabel("Total trial time (s)")
    plt.ylabel("Maximum absolute lane position (m)")
    plt.title("Bonus A: fixed steering after every three words")
    plt.legend()
    plt.tight_layout()
    plt.savefig("bonus_threeWords_comparison.png", dpi=300)
    plt.close()
    print("Bonus comparison saved as: bonus_threeWords_comparison.png")
    return results


# bonusResults = runBonusThreeWords(100)
# 

    




# section3AResults = runSimulations(100)
