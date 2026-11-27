### 
### This code is developed by Christian P. Janssen of Utrecht University
### It is intended for students from the Master's course Cognitive Modeling
### Large parts are based on the following research papers:
### Janssen, C. P., & Brumby, D. P. (2010). Strategic adaptation to performance objectives in a dual‐task setting. 
# Cognitive science, 34(8), 1548-1560. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1551-6709.2010.01124.x
### Janssen, C. P., Brumby, D. P., & Garnett, R. (2012). Natural break points: 
# The influence of priorities and cognitive and motor cues on dual-task interleaving. 
# Journal of Cognitive Engineering and Decision Making, 6(1), 5-29. https://journals.sagepub.com/doi/abs/10.1177/1555343411432339
###
### If you want to use this code for anything outside of its intended purposes 
# (training of AI students at Utrecht University), please contact the author:
### c.p.janssen@uu.nl



### 
### import packages
###

import matplotlib.pyplot as plt
import numpy as np

###
###
### Global parameters. These can be called within functions to change (Python: make sure to call GLOBAL)
###
###


###
### Car / driving related parameters
###
steeringUpdateTime = 250    #in ms ## How long does one steering update take? 
#(250 ms consistent with Salvucci 2005 Cognitive Science)
timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
startingPositionInLane = 0.27 			#assume that car starts already slightly away from 
#lane centre (in meters) (cf. Janssen & Brumby, 2010)


#parameters for deviations in car drift due the simulator environment: See Janssen & Brumby (2010) page 1555
gaussDeviateMean = 0
gaussDeviateSD = 0.13 ##in meter/sec



### The car is controlled using a steering wheel that has a maximum angle. 
# Therefore, there is also a maximum to the lateral velocity coming from a steering update
maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
minLateralVelocity = -1* maxLateralVelocity

startvelocity = 0 	#a global parameter used to store the lateral velocity of the car


###
### Switch related parameters
###
retrievalTimeWord = 200   #ms. ## How long does it take to think of the next word when
#interleaving after a word (time not spent driving, but drifting)
retrievalTimeSentence = 300 #ms. ## how long does it take to retrieve 
#a sentence from memory (time not spent driving, but drifting)



###
### parameters for typing task
###
timePerWord = 0  ### ms ## How much time does one word take
wordsPerMinuteMean = 39.33   # parameters that control typing speed: when typing two fingers, 
#on average you type this many words per minute. From Jiang et al. (2020; CHI)
wordsPerMinuteSD = 10.3 ## this is the standard deviation (Jiang et al, 2020)


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



##calculates if the car is not accelerating (m/s) more than 
# it should (maxLateralVelocity) or less than it should (minLateralVelocity)  
# (done for a vector of numbers)
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
	

## Function to determine lateral velocity (controlled with steering wheel) 
# based on where car is currently positioned. 
# See Janssen & Brumby (2010) for more detailed explanation.
## Lateral velocity update depends on current position in lane. 
# Intuition behind function: the further away you are, 
# the stronger the correction will be that a human makes
def vehicleUpdateActiveSteering(LD):

	latVel = 0.2617 * LD*LD + 0.0233 * LD - 0.022
	returnValue = velocityCheckForVectors(latVel)
	return returnValue ### in m/s
	


### function to update lateral deviation in cases where the driver is NOT steering actively 
# (when they are distracted by typing for example). 
# Draw a value from a random distribution. This can be added to the position where the car is already.
def vehicleUpdateNotSteering():
    
    global gaussDeviateMean
    global gaussDeviateSD 

    

    vals = np.random.normal(loc=gaussDeviateMean, scale=gaussDeviateSD,size=1)[0]
    returnValue = velocityCheckForVectors(vals)
    return returnValue   ### in m/s


### Function to run a trial. Needs to be defined by students (section 2 and 3 of assignment)
def runTrial(nrSentences = 10, nrSteeringMovementsWhenSteering = 4, interleaving="sentence"):
    
    global timePerWord
    resetParameters()

    minWPM = 14.9   # observed two-thumb range, Jiang et al. (2020)
    maxWPM = 58.4
    locPos = [] # stores calculated lane position values
    trialTime = [] #current trial time
    locColor = [] #stores color for plot 
    trialTime = 0      # ms
    position = startingPositionInLane
    dt = timeStepPerDriftUpdate / 1000 #length of one time step in seconds (50/1000=0.05s)
    
    nrWordsPerSentence = np.random.randint(15,21) 
    #transformed amount of words per sentence from static to uniform random draw

    
    typing_speed = np.random.normal(loc=wordsPerMinuteMean, scale=wordsPerMinuteSD)
    while not (minWPM <= typing_speed <= maxWPM):
        typing_speed = np.random.normal(loc=wordsPerMinuteMean, scale=wordsPerMinuteSD)

    if interleaving == "word":

        timePerWord = 60000/typing_speed        #for a conversion to miniseconds (60000 ms in a minute)
        typingTime = 0   
        doneUpdates = 0
        for sentence in range(nrSentences):
            for word in range(nrWordsPerSentence): #nested loop for each word over all sentences
                #typing:no steering car drifts
                wordTime = timePerWord + retrievalTimeWord
                if word == 0:
                    wordTime += retrievalTimeSentence

                typingTime += wordTime
                nUpdates = int(typingTime // timeStepPerDriftUpdate) - doneUpdates
                doneUpdates += nUpdates

                for _ in range(nUpdates):
                    position += vehicleUpdateNotSteering() * dt #to seconds
                    locPos.append(position)
                    locColor.append("red")
                trialTime += wordTime

                 # steering, except after the very last word
                lastWord = (sentence == nrSentences - 1 and word == nrWordsPerSentence - 1)
                if not lastWord:
                    for _ in range(nrSteeringMovementsWhenSteering):
                        # once per 250 ms; steer toward center
                        latVel = vehicleUpdateActiveSteering(abs(position))
                        latVel = -np.sign(position) * latVel
                        for _ in range(steeringUpdateTime // timeStepPerDriftUpdate):
                            position += latVel * dt
                            locPos.append(position)
                            locColor.append("blue")
                        trialTime += steeringUpdateTime
        return trialTime, locPos, locColor

    if interleaving == "sentence":

        timePerWord = 60000/typing_speed        #for a conversion to miniseconds (60000 ms in a minute)
        typingTime = 0
        doneUpdates = 0

        for sentence in range(nrSentences):
            time_sentence = retrievalTimeSentence + timePerWord * nrWordsPerSentence
            
            typingTime += time_sentence
            nUpdates = int(typingTime // timeStepPerDriftUpdate) - doneUpdates
            doneUpdates += nUpdates

            
            for _ in range(nUpdates):
                position += vehicleUpdateNotSteering() * dt #dt for measurement in seconds 
                locPos.append(position)
                locColor.append("red")
            trialTime += time_sentence

            # steering, except after the very last sentence
            lastSentence = sentence == nrSentences - 1
            if not lastSentence:
                for _ in range(nrSteeringMovementsWhenSteering):
                    latVel = vehicleUpdateActiveSteering(abs(position))
                    latVel = -np.sign(position) * latVel  # steer based on side of lane
                    for _ in range(steeringUpdateTime // timeStepPerDriftUpdate):
                        position += latVel * dt
                        locPos.append(position)
                        locColor.append("blue")
                    trialTime += steeringUpdateTime

        return trialTime, locPos, locColor

    if interleaving == "drivingOnly":
        
        wordTime = 60000/typing_speed
        total_time = nrSentences * (retrievalTimeSentence + nrWordsPerSentence * wordTime )
        nUpdates = int(total_time // timeStepPerDriftUpdate)
        stepsPerSteering = steeringUpdateTime // timeStepPerDriftUpdate    

        for k in range(nUpdates):
            if k % stepsPerSteering == 0:
                latVel = vehicleUpdateActiveSteering(abs(position))
                latVel = -np.sign(position) * latVel
            position += latVel * dt
            locPos.append(position)
            locColor.append("green")
        trialTime = total_time

        return trialTime, locPos, locColor
    
    if interleaving == "none":

        timePerWord = 60000 / typing_speed  # ms per word
        total_typing_time = nrSentences * (retrievalTimeSentence + nrWordsPerSentence * timePerWord)
        nUpdates = int(total_typing_time // timeStepPerDriftUpdate)

        for _ in range(nUpdates):
            position += vehicleUpdateNotSteering() * dt  # dt in seconds
            locPos.append(position)
            locColor.append("yellow")
        trialTime = total_typing_time

        return trialTime, locPos, locColor

def plotTrial(trialTime, locPos, locColor, interleaving = "none"):
    t = (np.arange(len(locPos)) + 1) * timeStepPerDriftUpdate   # ms
    meanPos = np.mean(locPos)
    MaxPos = np.max(np.abs(locPos))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(t, locPos, c=locColor, s=2)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Lane position (m)")
    ax.set_title(f"Total trial time = {trialTime:.0f} ms; "
              f"Mean position on the road = {meanPos:.3f} m; "
              f"Max position on the road (Absolute) = {MaxPos:.3f} m",
              fontsize=8)
    fig.tight_layout()
    if runTrial(interleaving = "word"):
        plt.savefig(f"output/{interleaving}_{trialTime:.0f}_{meanPos:.3f}_{MaxPos:.3f}.png")
    
    plt.show()
    plt.close(fig)


### function to run multiple simulations
def runSimulations(nrSims=100):
    conditions = ["word", "sentence", "drivingOnly", "none"]

    totalTime = []
    meanDeviation = []
    maxDeviation = []
    Condition = []

    for condition in conditions:
        for _ in range(nrSims):
            trialTime, locPos, locColor = runTrial(interleaving=condition)
            #plotTrial(trialTime, locPos, locColor, condition)
            totalTime.append(trialTime)
            meanDeviation.append(np.mean(np.abs(locPos)))
            maxDeviation.append(np.max(np.abs(locPos)))
            Condition.append(condition)

    return totalTime, meanDeviation, maxDeviation, Condition

np.random.seed(49)
totalTime, meanDeviation, maxDeviation, Condition  = runSimulations()
    
def plotResults(totalTime, meanDeviation, maxDeviation, Condition):
    totalTime = np.array(totalTime)
    maxDeviation = np.array(maxDeviation)
    Condition = np.array(Condition)

    styles = {
        "word":        ("o", "blue"),
        "sentence":    ("^", "red"),
        "drivingOnly": ("s", "green"),
        "none":        ("x", "black"),
    }

    fig, ax = plt.subplots(figsize=(9, 6))

    for condition, (marker, color) in styles.items():
        mask = Condition == condition
        times = totalTime[mask]
        deviations = maxDeviation[mask]

        ax.scatter(times, deviations, marker=marker, color="grey",
                   s=25, alpha=0.5)

        timeSD = np.std(times, ddof=1)
        deviationSD = np.std(deviations, ddof=1)
        timeMean = np.mean(times)
        deviationsMean = np.mean(deviations)

        ax.errorbar(np.mean(times), np.mean(deviations),
                    xerr=timeSD, yerr=deviationSD,
                    fmt=marker, color=color,
                    markersize=11, markeredgewidth=2,
                    elinewidth=1.5, capsize=5, zorder=3,
                    label=condition)

        print(f"{condition}: time SD = {timeSD:.1f} ms, "
              f"max deviation SD = {deviationSD:.3f} m, "
              f"time mean = {timeMean:.3f} ms, "
              f"max deviations mean = {deviationsMean:.3f} m")

    ax.set_xlabel("Total trial time (ms)")
    ax.set_ylabel("Maximum lateral deviation (m)")
    ax.set_title("Maximum lateral deviation by total trial time")
    ax.legend(title="Condition (colour: mean ± 1 SD; grey: trials)")
    fig.tight_layout()
    plt.show()

plotResults(totalTime, meanDeviation, maxDeviation, Condition)

print("Script finished!")