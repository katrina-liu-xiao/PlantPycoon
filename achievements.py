#   This file is for the achievements page of Plant Pycoon


class Achievement(object):
    def __init__(self,name,target,level):
        self.name = name
        # Target is the number that a property needs to be reached for this acheivements.
        self.target = target 
        # Level is the current level that an achievement is. If an achievement 
        # is reached, a higher level of this achievement will be unlocked.
        self.level = level
        #   Progress is a factor of how much of this achievement is completed.
        self.progress = 0
    def __eq__(self,other):
        return isinstance(other, Achievement) and (self.name == other.name) \
        and (self.target == other.target) and (self.level == other.level)
    def __hash__(self,other):
        return hash((self.name,self.target,self,level))
    def __repr__(self):
        return "%s level %d: %d/%d" %(self.name,self.level,self.progress,self.target)
    def gain(self,num):
        self.progress += num
        while self.complete():
            self.target *= 5
            self.level += 1
    def ratio(self):
        return self.progress/self.level
    def complete(self):
        return self.target <= self.progress









 
   
   
