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

def runTrial(nrWordsPerSentence =5,nrSentences=3,nrSteeringMovementsWhenSteering=2, interleaving="word",runNumber=None): 
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

     if interleaving == "word":
        print("Running word strategy")
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
                if not isLastWord:
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

            # 连续输入当前句子的全部单词
            for wordIndex in range(nrWordsPerSentence):
                # sentence 策略不计算 retrievalTimeWord
                wordDuration = timePerWord

                # 每句话开始时，只计算一次句子提取时间
                if wordIndex == 0:
                    wordDuration += retrievalTimeSentence

                # 输入期间没有主动驾驶，所以车辆漂移
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

            # 整句话输入完毕后，才切回驾驶
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

                    # 车辆在右侧就向左修正，在左侧就向右修正
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


     print("Total typing time:", round(trialTime, 2), "ms")
     print("Number of stored positions:", len(locPos))
     print("Current lane position:", round(currentPosition, 4), "m")
     print("Final time:", trialTime)
     print("Final position:", currentPosition)
     print("Strategy:", interleaving)

     timeValues = numpy.arange(len(locPos)) * timeStepPerDriftUpdate

     absolutePositions = [abs(position) for position in locPos]

     meanPosition = numpy.mean(absolutePositions)
     maxPosition = max(absolutePositions)
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
     plt.close()

     print("Plot saved as:", plotFileName)
     print("Mean absolute position:", round(meanPosition, 4), "m")
     print("Max absolute position:", round(maxPosition, 4), "m")

     return trialTime, locPos, locColor

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
for runNumber in range(1, 11):
    print("\nRunning word trial:", runNumber)

    runTrial(
        nrWordsPerSentence=17,
        nrSentences=10,
        nrSteeringMovementsWhenSteering=4,
        interleaving="word",
        runNumber=runNumber
    )
	
	




### function to run multiple simulations. Needs to be defined by students (section 3 of assignment)
def runSimulations(nrSims = 100):
    print("hello world")



	




