class Character():
    def __init__(self, id):
        self.id = id
        
    def __str__(self):
        return f"Nome: {self.id}"