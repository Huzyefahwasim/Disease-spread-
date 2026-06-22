import numpy as np

class DiseaseSimulation:
    def __init__(self, population=1000000, initial_infected=50, beta=0.25, sigma=0.1, gamma=0.05, mu=0.01, days=100):
        self.population = population
        self.initial_infected = initial_infected
        self.beta = beta   # Transmission rate
        self.sigma = sigma # Incubation rate (rate of E -> I)
        self.gamma = gamma # Recovery rate (rate of I -> R)
        self.mu = mu       # Mortality rate (rate of I -> D)
        self.days = days
        
        self.S = [population - initial_infected]
        self.E = [0]
        self.I = [initial_infected]
        self.R = [0]
        self.D = [0]
        
    def run(self):
        for _ in range(1, self.days):
            S_prev = self.S[-1]
            E_prev = self.E[-1]
            I_prev = self.I[-1]
            R_prev = self.R[-1]
            D_prev = self.D[-1]
            
            # New transitions
            new_exposed = (self.beta * S_prev * I_prev) / self.population
            new_infectious = self.sigma * E_prev
            new_recoveries = self.gamma * I_prev
            new_deaths = self.mu * I_prev
            
            self.S.append(max(0, S_prev - new_exposed))
            self.E.append(max(0, E_prev + new_exposed - new_infectious))
            self.I.append(max(0, I_prev + new_infectious - new_recoveries - new_deaths))
            self.R.append(min(self.population, R_prev + new_recoveries))
            self.D.append(min(self.population, D_prev + new_deaths))
            
        return {
            'Susceptible': self.S,
            'Exposed': self.E,
            'Infectious': self.I,
            'Recovered': self.R,
            'Dead': self.D
        }
