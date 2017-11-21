# Name: Wenkai Cui
# Email: wkcui@bu.edu
# a8task1.py. - Assignment 8, Task 1
#
# Task1 : Black-Scholes option pricing
#1
import math
from scipy.stats import norm

class BSOption:
    def __init__(self,s,x,t,sigma,rf,div):
        '''
        s (the current stock price in dollars), 
        x (the option strike price),
        t (the option maturity time in years), 
        sigma (the annualized standard deviation of returns), 
        rf (the annualized risk free rate of return),
        div (the annualized dividend rate; assume continuous dividends rate), 
        '''
        self.s=s
        self.x=x
        self.t=t
        self.sigma=sigma
        self.rf=rf
        self.div=div
    def __repr__(self):
        return 's = $%.2f, x = $%.2f, t = %.2f (years), sigma = %.3f, rf = %.3f, div = %.2f' %(self.s,self.x,self.t,self.sigma,self.rf,self.div)

#2
    def d1(self):
        return (1/(self.sigma*self.t**0.5))*(math.log(self.s/self.x)+(self.rf-\
                self.div+self.sigma**2/2)*self.t)
    def d2(self):
        return self.d1()-self.sigma*self.t**0.5
    def nd1(self):
        ''' N(d1)'''
        return norm.cdf(self.d1())
    def nd2(self):
        ''' N(d2)'''
        return norm.cdf(self.d2())


#3
    def value(self):
        print('Cannot calculate value for base class BSOption.')
        return 0
    def delta(self):
        print('Cannot calculate delta for base class BSOption.')
        return 0
    

#4
class BSEuroCallOption(BSOption):
    ''' inherits from the base class BSOPtion and implements the pricing
    algorithm for a European-style call option'''
    def init__(self,s,x,t,sigma,rf,div):
        BSOption.__init__(self,s,x,t,sigma,rf,div)
    def value(self):
        '''European call option’s value'''
        return self.nd1()*self.s*math.exp(-self.div*self.t)-self.nd2()*self.x*\
                math.exp(-self.rf*self.t)
    def __repr__(self):
        return 'BSEuroCallOption, value = $%.2f,\nparameters = (%s)'%(self.value(),BSOption.__repr__(self))
    def delta(self):
        '''delta as an approximation of the change in the value of this option 
        for a $1 change in price in the underlying stock'''
        return self.nd1()
    

#5
class BSEuroPutOption(BSOption):
    ''' inherits from the base class BSOPtion and implements the pricing algorithm 
    for a European-style put option. '''
    def init__(self,s,x,t,sigma,rf,div):
        BSOption.__init__(self,s,x,t,sigma,rf,div)
    def value(self):
        '''European put option’s value'''
        return norm.cdf(-self.d2())*self.x*math.exp(-self.rf*self.t)-norm.cdf(-self.d1())*self.s*\
                math.exp(-self.div*self.t)
    def __repr__(self):
        return 'BSEuroPutOption, value = $%.2f,\nparameters = (%s)'%(self.value(),BSOption.__repr__(self))
    def delta(self):
        return self.nd1()-1
            
#7
def generate_option_value_table(s, x, t, sigma, rf, div):
    call=BSEuroCallOption(s, x, t, sigma, rf, div)
    put=BSEuroPutOption(s, x, t, sigma, rf, div)
    print(call)
    print(put)
    print('''\nChange in option values w.r.t. change in stock price:
   price        call value  put value   call delta    put delta''')
    for p in range(s-10,s+11,1):
        call=BSEuroCallOption(p, x, t, sigma, rf, div)
        put=BSEuroPutOption(p, x, t, sigma, rf, div)
        print('$   %6.2f   $    %6.2f   $   %6.2f     %6.4f       %7.4f'%(p,call.value(),put.value(),call.delta(),put.delta()))


#8
def calculate_implied_volatility(option, value):
    '''calculate the implied volatility of an observed option'''
    
    sd=0
    su=4
    option.sigma=2
    dif=value-option.value()
    while abs(dif)>0.001:
        if dif>0:
            sd=(sd+su)/2
            option.sigma=(sd+su)/2
        if dif < 0:
            su=(sd+su)/2
            option.sigma=(sd+su)/2
#        print(su,sd,'sigma=',option.sigma,'estimte/value=',option.value())
        dif= value-option.value()
    return option.sigma
    
    

#call = BSEuroCallOption(116.67, 75, 28/365, 0.5, 0.00, 0.00)
#put = BSEuroPutOption(116.67, 100, 28/365, 0.01, 0.00, 0.00)

#option = BSOption(100, 100, 0.25, 0.3, 0.06, 0.00)
##print(option)
#call = BSEuroCallOption(100, 100, 1, 0.30, 0.06, 0.00)
##print(call)
#put = BSEuroPutOption(100, 100, 1, 0.30, 0.06, 0.00)