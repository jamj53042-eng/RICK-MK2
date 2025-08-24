class Config:
    def __init__(self):
        self.version = "0.1"
        self.mode = "sandbox"
    
    def __repr__(self):
        return f"<Config version={self.version} mode={self.mode}>"
