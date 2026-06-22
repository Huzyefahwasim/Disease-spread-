class DiseaseSimulation:
    def __init__(self, population=1000000, initial_infected=50, beta=0.25, gamma=0.1, days=100):
        self.population = population
        self.initial_infected = initial_infected
        self.beta = beta
        self.gamma = gamma
        self.days = days
        
        self.S = [population - initial_infected]
        self.I = [initial_infected]
        self.R = [0]
        
    def run(self):
        for _ in range(1, self.days):
            new_infections = (self.beta * self.S[-1] * self.I[-1]) / self.population
            new_recoveries = self.gamma * self.I[-1]
            
            self.S.append(max(0, self.S[-1] - new_infections))
            self.I.append(max(0, self.I[-1] + new_infections - new_recoveries))
            self.R.append(min(self.population, self.R[-1] + new_recoveries))
            
        return {
            'Susceptible': self.S,
            'Infected': self.I,
            'Recovered': self.R
        }
