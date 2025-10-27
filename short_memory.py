class ShortMemoryService:
    def __init__(self, max_memory):
        self.history = []
        self.max_memory = max_memory

    def append(self, role, content):
        # remove first element if reach max memory
        if len(self.history) > self.max_memory:
            self.history.pop(0)
        
        self.history.append({
            "role": role,
            "content": content
        })
    
    def build_prompt(self, number):
        result = ""
        
        for h in self.history[-number:]:
            result += f"{h['role']}: {h['content']}\n"
        
        return result