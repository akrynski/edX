# -*- coding: utf-8-sig -*-
# Problem Set 8: Simulating the Spread of Disease and Virus Population Dynamics 
import matplotlib
import numpy
import random
import pylab
#from ps8b_precompiled_27 import *
import pdb
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """
    
'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        
        return float(self.maxBirthProb)

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return float(self.clearProb)

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() < self.getClearProb():
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.getMaxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if random.random() <= (self.getMaxBirthProb() * (1 - popDensity)):
            return SimpleVirus(self.getMaxBirthProb(),self.getClearProb())
        else:
            raise NoChildException()
        



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.currentVirusesPopulation = []
        self.popDensity = 0.0

    def getPopDensity(self):
        """returns viruses/maxPop ratio"""
        return self.popDensity
    def setPopDensity(self, ratio):
        """sets viruses/maxPop ratio"""
        self.popDensity = ratio

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        #inicjuj zmienną child
        child = None
        children = []
        #ustal, które wirusy przeżyją: doesClear na każdej instancjj SimpleVirus
        #mamy daną listę wirusów -getViruses()- i populację (ilość) - getMaxPop()
        vircopy = self.viruses[:] 
        for virus in vircopy:
            #for population in range(self.getMaxPop()):
                if not virus.doesClear():
                    self.currentVirusesPopulation.append(virus) 
        self.viruses = self.currentVirusesPopulation #tylko te co przeżyły
        #mając pełną listę wirusów obliczamy ratio
        self.setPopDensity(self.getTotalPop()/float(self.getMaxPop()))

        #mając te, które przeżyją wysyłamy je do reprodukcji ;)
        # (SimpleVirus)SimpleVirus.reproduce(popDensity)
        for virus in self.currentVirusesPopulation:
            try:
                child = virus.reproduce(self.getPopDensity())
            except NoChildException:
                pass
            else:
                #dodaj potomka
                children.append(child)
            #finally:
        #po wyjściu z pętli dodajemy potomki
        self.viruses.extend(children)
        self.currentVirusesPopulation = [] #????

        
        return self.getTotalPop()
                


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    
    simulationWithoutDrug(100, 1000, 0.1, 0.05, 10)
    """
##    def divide(a):
##        return a/float(numTrials)
    
    def labelPlot():
        pylab.title("Average viruses population in patient's body")
        pylab.xlabel('Time unit')
        pylab.ylabel('Viruses/numTrials ratio')
        pylab.legend(bbox_to_anchor=(0.3, 0.2), loc=2, borderaxespad=0.,\
                     title="maxBirthProb=0.1\nclearProb=0.001")


    viruses = []
    averages = []
    results = []
    for i in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))

    patient = Patient(viruses, maxPop)

    for i in range(numTrials):
        totalPop=[]
        for i in range(300):
            totalPop.append(float(patient.update()))
        results.append(totalPop)
    #averages = map(divide,totalPop)
    averages = [sum(sublist)/float(len(results)) for sublist in zip(*results)]
 
        
    #makePlot(range(numTrials), averages)
    pylab.plot(range(0,300), averages, label='Population of viruses')
    
    labelPlot()
    pylab.show()

    



#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        UWAGA! MOGĄ PODAĆ NIE ISTNIEJĄCY W LIŚCIE
        """
        if self.resistances.get(drug, 0):
            return True
        else: return False
##        if not drug in self.resistances.keys():
##            raise AssertionError
##            if drug in self.resistances:
##                return self.resistances[drug]
##            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.getMaxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb, clearProb, and mutProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        #pdb.set_trace()
        res = self.getResistances()
        childres = {}#BUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!! forgotten child ;)
        for drug in activeDrugs:
            if not res[drug]:
                 raise NoChildException()
                              
        if random.random() <= (self.getMaxBirthProb() * (1 - popDensity)):
        
            for d in res:
               if random.random() < self.getMutProb():
                   childres[d] = not(self.resistances[d])
               else: #BUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!! forgotten child ;)
                   childres[d] = self.resistances[d]#BUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!! forgotten child ;)
        else:
            raise NoChildException() 
            
             
        return ResistantVirus(self.getMaxBirthProb(),
                              self.getClearProb(),
                              childres,#BUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!! forgotten child ;)
                              self.getMutProb())                
##        for drug in activeDrugs:
##            if not self.isResistantTo(drug):
##                raise NoChildException()
## 
##        prob = random.random()
##        if prob < self.maxBirthProb * (1 - popDensity):
##            childResistances = {}
##            for drug in self.resistances.keys():
##                resistanceProb = random.random()
##                if resistanceProb < self.mutProb:
##                    childResistances[drug] = not self.resistances[drug]
##                else:
##                    childResistances[drug] = self.resistances[drug]
## 
##            child = ResistantVirus(self.maxBirthProb, self.clearProb, childResistances, self.mutProb)
##            return child
##        raise NoChildException()
   

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        #print 'got a new drug: '+ newDrug
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)
        #print self.drugs


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        #MOJE
        population = []      
        virlist = self.getViruses()
        for virus in virlist:
            test = True            
            for drug in drugResist:
                test = test and virus.isResistantTo(drug)
            if test:
                population.append(1)
        return sum(population)
## FROM FORUM
##    def getResistPop(self, drugResist):
##        population = []
##        for virus in self.viruses:
##            for drug in drugResist:
##                if not virus.isResistantTo(drug):
##                    try:
##                        population.remove(virus) # removes virus if virus in population
##                    except ValueError: # if virus not in population
##                        pass
##                    break # no point in checking other drugs
##                elif virus in population:
##                    pass
##                else: # only if virus is not in population
##                    population.append(virus)
##
##        return len(population)

##    def getResistPop(self, drugResist):
##        resistantPopulation = 0
##        for virus in self.viruses:
##            resistance = 0
##            for drug in drugResist:
##                if virus.isResistantTo(drug) == True:
##                    resistance += 1
##            if resistance == len(drugResist):
##                resistantPopulation += 1
##        return resistantPopulation               


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        child = None
        children = []
        self.currentVirusesPopulation = []
        vircopy = self.viruses[:] #kopia listy instancji

        #pdb.set_trace()

        for virus in vircopy:
            
            if not virus.doesClear():
                    self.currentVirusesPopulation.append(virus)
               
        self.viruses = self.currentVirusesPopulation #update list
        self.setPopDensity(self.getTotalPop()/float(self.getMaxPop())) #calculate density
        #REMARK
        #there is no get/setPopDensity method in Patient class of PS3 6.0.0.2x
        #to solve this copy those setters/getters to TreatedPatient class
        for virus in self.currentVirusesPopulation:
           try: #checked, prescriptions ok
               child = virus.reproduce(self.getPopDensity(), self.getPrescriptions())#check reproduction
           except NoChildException:
               pass
           else:
                   children.append(child) #add to offsprings
##        currentPopulation.extend(children) #nowe!
##        self.viruses = currentPopulation       #nowe - ale to nic nie zmienia, po staremu mniej kodu
        self.viruses.extend(children) #add offsprings - stare

        #currentPopulation = []
        return self.getTotalPop()
    
               


#
# PROBLEM 5

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):#,prescript):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
## FROM FORUM - dgershman
    #virusPops = []
    #resVirusPops = []
    #for trial in range(numTrials):
    #    virusList = []
    #    for virus in range(numViruses):
    #        newVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    #        virusList.append(newVirus)
    #    newPatient = TreatedPatient(virusList,maxPop)
    #    for x in range(150):
    #        newPatient.update()
    #        if virusPops == [] or len(virusPops) == x:
    #            virusPops.append(newPatient.getTotalPop())
    #        else:
    #            virusPops[x] += newPatient.getTotalPop()
    #        if resVirusPops == [] or len(resVirusPops) == (x):
    #            resVirusPops.append(newPatient.getResistPop(['guttagonol']))
    #        else:
    #            resVirusPops[x] += newPatient.getResistPop(['guttagonol'])
    #    newPatient.addPrescription('guttagonol')
    #    for y in range(150,300):
    #        newPatient.update()
    #        if len(virusPops) == (y):
    #            virusPops.append(newPatient.getTotalPop())
    #        else:
    #            virusPops[y] += newPatient.getTotalPop()
    #        if len(resVirusPops) == (y):
    #            resVirusPops.append(newPatient.getResistPop(['guttagonol']))
    #        else:
    #            resVirusPops[y] += newPatient.getResistPop(['guttagonol'])
    #popAverage = []
    #resPopAverage = []
    #for p in range(len(virusPops)):
    #    popAverage.append(virusPops[p]/float(numTrials))
    #for r in range(len(resVirusPops)):
    #    resPopAverage.append(resVirusPops[r]/float(numTrials))
    #pylab.plot(range(300),popAverage,label='Total average virus pop. over ' + str(numTrials) + ' trials')
    #pylab.plot(range(300),resPopAverage,'r-',label='Average guttagonol-resistant virus pop. over ' + str(numTrials) + ' trials')
    #pylab.title('Average Virus Population Size in a Treated Patient over 300 Days')
    #pylab.xlabel('Days')
    #pylab.ylabel('Average virus population')
    #pylab.legend()
    #pylab.show()

    # MOJE - the first version of 6.00x - bad, although results are very near
#    def labelPlot(title,xlab,ylab,legtitle):
#        '''tytuł, labelX, labelY, tytuł dla legendy'''
#        pylab.title(title)
#        pylab.xlabel(xlab)
#        pylab.ylabel(ylab)
#        pylab.legend(title=legtitle,loc=0)
#
#    viruses = []
#    averages = []
#    results = []
#    taverages=[]
#    tresults=[]
#       
#    for i in range(numViruses):
#        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
#
#    for i in range(numTrials): #FOR EACH OF NUM TRIALS
#        totalPopTmp=[]
#        resistantPopTmp=[]
#        
#        patient = TreatedPatient(viruses,maxPop) #INSTANTIES A PATIENT
#        
#        for i in range(prescript+150):
#            totalPopTmp.append(float(patient.update())) #after loop I get [tot1, tot2...tot150]
#            resistantPopTmp.append(patient.getResistPop(["guttagonol"])) # here the same but resistant popul. after each update
#            if i == prescript:
#                patient.addPrescription("guttagonol") # ADD PRESCRIPTION
#        results.append(totalPopTmp) # at the end of loop add list to list of lists
#        tresults.append(resistantPopTmp) #the same as above
#        
#    #after numTrials I have results = [[tot1/1, tot2/1 ... tot150/1][tot1/2, tot2/2 ... tot150/2]...[tot1/numTrials, tot2/numTrials ...tot150/numTrials]]
#    #the same for tresults where I have resistant population tables
#    #now I compute average values
#    averages = [sum(sublist)/float(len(results)) for sublist in zip(*results)]        
#    taverages = [sum(sublist)/float(len(tresults)) for sublist in zip(*tresults)]
#    
#    pylab.plot(averages,label="Total virus population")              
#    pylab.plot(taverages,'r--', label="Resistant to guttagonol")
#    labelPlot("Average population of of viruses in the body being treated", "Time step", "viruses/numTrials ratio", \
#              "maxBirthProb: "+str(maxBirthProb)+"\nclearProb: "+str(clearProb)+"\nmutProb: "+str(mutProb))
#    pylab.text(prescript,200,"Guttagonol prescripted \nat step "+str(prescript))
#    pylab.grid(True)
#    #pylab.draw()
#    
#
## simulationWithDrug(100, 1000, .1, 0.05, {"guttagonol": False}, 0.005, 100)
#if __name__ == '__main__':
#    prescripts = [300,150,75,0]
#    for sim in prescripts:
#         simulationWithDrug(100, 1000, .1, 0.05, {"guttagonol": False}, 0.005, 100, sim)
#    
#    pylab.show()    
#




    # MOJE Problem Set 3 from 6.0.0.2x solved after 2 years :) :P
    def labelPlot(title,xlab,ylab,legtitle):
        '''tytuł, labelX, labelY, tytuł dla legendy'''
        pylab.title(title)
        pylab.xlabel(xlab)
        pylab.ylabel(ylab)
        pylab.legend(title=legtitle,loc=0)


    averages = []
    results = []
    taverages=[]
    tresults=[]
       
    for i in range(numTrials):#Start a for loop with a range of number of trial. 
        #Create a list of virus using a list comprehension with range number of virus.
        viruses = []
        [viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)) for i in range(numViruses)]#
        totalPopTmp=[]
        resistantPopTmp=[]
        #Create Treated patient instance with the virus list
        patient = TreatedPatient(viruses,maxPop) #INSTANTIES A PATIENT
        #Start a for loop with range 150 naming the variable index. 
        #add to the index of each list the value of the patient update 
        #or the patient resistant population (in the last case passing as parameter a list containing 'guttagonol'
        for i in range(150):
            totalPopTmp.append(float(patient.update())) #after loop I get [tot1, tot2...tot150]
            resistantPopTmp.append(patient.getResistPop(["guttagonol"])) # here the same but resistant popul. after each update
        results.append(totalPopTmp) # at the end of loop add list to list of lists
        tresults.append(resistantPopTmp) #the same as above
        
        patient.addPrescription("guttagonol") # ADD PRESCRIPTION
        for i in range(150,300):
            totalPopTmp.append(float(patient.update())) #after loop I get [tot1, tot2...tot150]
            resistantPopTmp.append(patient.getResistPop(["guttagonol"])) # here the same but resistant popul. after each update
        results.append(totalPopTmp) # at the end of loop add list to list of lists
        tresults.append(resistantPopTmp) #the same as above
        
    #after numTrials I have results = [[tot1/1, tot2/1 ... tot150/1][tot1/2, tot2/2 ... tot150/2]...[tot1/numTrials, tot2/numTrials ...tot150/numTrials]]
    #the same for tresults where I have resistant population tables
    #now I compute average values
    averages = [sum(sublist)/float(len(results)) for sublist in zip(*results)]        
    taverages = [sum(sublist)/float(len(tresults)) for sublist in zip(*tresults)]
    
    pylab.plot(averages,label="Total virus population")              
    pylab.plot(taverages,'r--', label="Resistant to guttagonol")
    #pylab.plot(tresults,'g--', label="Resistant to guttagonol")
    labelPlot("Average population of of viruses in the body being treated", "Time step", "viruses/numTrials ratio", \
              "maxBirthProb: "+str(maxBirthProb)+"\nclearProb: "+str(clearProb)+"\nmutProb: "+str(mutProb))
    #pylab.text(prescript,200,"Guttagonol prescripted \nat step "+str(prescript))
    pylab.grid(True)
    #pylab.draw()
    #print tresults
    pylab.show() 

# simulationWithDrug(100, 1000, .1, 0.05, {"guttagonol": False}, 0.005, 100)
if __name__ == '__main__':
#    prescripts = [0]
#    for sim in prescripts:
    simulationWithDrug(100, 1000, .1, 0.05, {"guttagonol": False}, 0.005, 100)
    #simulationWithDrug(100, 1000, .8, 0.1, {"guttagonol": False}, 0.8, 1)
    

      


