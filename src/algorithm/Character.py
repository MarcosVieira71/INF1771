class Character():
    def __init__(self, id, power):
        self.id = id
        self.lives = 5
        self.power = power
    
    def decreaseHP(self):
        self.lives-=1
    
    def __str__(self):
        return f"Nome: {self.id} Poder: {self.power}"
