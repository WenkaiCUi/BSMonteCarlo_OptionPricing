# Name: Wenkai Cui
# Email: wkcui@bu.edu
# a8task2.py. - Assignment 8, Task 2
#
# Task 2: Monte-Carlo Option Pricing
#1
import math
import random
import statistics as stat

class MCStockOption:
    '''encapsulate the idea of a Monte Carlo stock option, and contain all of the
    data members required to run stock-price simulations and calculate the option’s payoff
    '''
#1
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        '''
        s, which is the initial stock price
        x, which is the option’s exercise price
        r, which is the (expected) mean annual rate of return on the underlying stock
        sigma, which is the annual standard deviation of returns on the underlying stock
        t, which is the time to maturity for the option
        nsteps, which is the number of discrete time steps with which to evaluate the option
        ntrials, which is the number of trials to run with this option
        '''
        self.s=s
        self.x=x
        self.r=r
        self.sigma=sigma
        self.t=t
        self.nsteps=nsteps
        self.ntrials=ntrials
    def __repr__(self):
        return 'MCStockOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)

#2
    def generate_stock_prices(self):
        '''generate and return a list containing simulated stock prices over 
        the course of this option’s lifetime t'''
        
        dt = self.t/self.nsteps
        lst=[self.s]
        for i in range(self.nsteps):
            z=random.gauss(0, 1)
            dr=(self.r-self.sigma**2/2)*dt+z*self.sigma*dt**0.5
            lst+=[lst[-1]*math.exp(dr)]
            
        return lst
        
    
#3
    def  value(self):
        ''' return the value of the option'''
        print('Base class MCStockOption has no concrete implementation of .value(). # print statement')
        return 0
    
    

    def stderr(self):
        '''return the standard error of this option’s value'''
        
        if 'stdev' in dir(self):
            return self.stdev / math.sqrt(self.ntrials)
        return 0
    
#4
class MCEuroCallOption(MCStockOption):
    ''' European call option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCEuroCallOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self):
        trials=[max(self.generate_stock_prices()[-1]-self.x,0)*\
                           math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean


#5
class MCEuroPutOption(MCStockOption):
    ''' European put option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCEuroPutOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self):
        trials=[max(self.x-self.generate_stock_prices()[-1],0)*\
                           math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean
    
#6
class MCAsianCallOption(MCStockOption):
    '''Asian call option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCAsianCallOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self):
        trials=[max(stat.mean(self.generate_stock_prices())-self.x,0)*math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean
    
#7
class MCAsianPutOption(MCStockOption):
    '''Asian put option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCAsianPutOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self): 
        trials=[max(self.x-stat.mean(self.generate_stock_prices()),0)*math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean
    
#8
class MCLookbackCallOption(MCStockOption):
    ''' look-back call option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCLookbackCallOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self): 
        trials=[max(max(self.generate_stock_prices())-self.x,0)*math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean


#9
class MCLookbackPutOption(MCStockOption):
    ''' look-back put option'''
    def __init__(self,s,x,r,sigma,t,nsteps,ntrials):
        MCStockOption.__init__(self,s,x,r,sigma,t,nsteps,ntrials)
    def __repr__(self):
        return 'MCLookbackPutOption, s=%.2f, x=%.2f  r=%.2f, sigma=%.2f, t=%.2f, nsteps=%.f, ntrials=%.f'%(self.s,self.x,self.r,self.sigma,self.t,self.nsteps,self.ntrials)
    def value(self): 
        trials=[max(self.x-min(self.generate_stock_prices()),0)*math.exp(-self.r*self.t) for i in range(self.ntrials)]
        self.mean = stat.mean(trials)
        self.stdev = stat.pstdev(trials)
        return self.mean


#option = MCStockOption(100, 100, 0.1, 0.3, 1, 5, 10)
#call = MCEuroCallOption(100, 100, 0.1, 0.3, 1, 100, 100000)
#put = MCEuroPutOption(100, 100, 0.1, 0.3, 1, 100, 100000)
#acall = MCAsianCallOption(100, 100, 0.10, 0.30, 1, 100, 1000)
#aput = MCAsianPutOption(100, 100, 0.10, 0.30, 1, 100, 1000)
#lcall = MCLookbackCallOption(100, 100, 0.10, 0.30, 1, 100, 1000)
#lput=MCLookbackPutOption(100, 100, 0.10, 0.30, 1, 100, 1000)
def test():
    print('****AC')
    acall = MCAsianCallOption(35, 30, 0.08, 0.25, 1, 100, 100000)
    print(acall.value())
    print(acall.stderr())
    acall = MCAsianCallOption(35, 40, 0.08, 0.40, 1, 100, 100000)
    print(acall.value())
    print(acall.stderr())
    print('****AP')
    aput = MCAsianPutOption(35, 30, 0.08, 0.25, 1, 100, 100000)
    print(aput.value())
    print(aput.stderr())
    aput = MCAsianPutOption(35, 40, 0.08, 0.40, 1, 100, 100000)
    print(aput.value())
    print(aput.stderr())
    print('****CBC')
    lcall = MCLookbackCallOption(35, 30, 0.08, 0.25, 1, 100, 100000)
    print(lcall.value())
    print(lcall.stderr())
    lcall = MCLookbackCallOption(35, 40, 0.08, 0.40, 1, 100, 100000)
    print(lcall.value())
    print(lcall.stderr())
    print('****CBP')
    lput = MCLookbackPutOption(35, 30, 0.08, 0.25, 1, 100, 100000)
    print(lput.value())
    print(lput.stderr())
    lput = MCLookbackPutOption(35, 40, 0.08, 0.40, 1, 100, 100000)
    print(lput.value())
    print(lput.stderr())
