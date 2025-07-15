class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, listener):
        """Подписывает слушателя на событие."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    async def emit(self, event, *args):
        """Вызывает слушателей для события и передает им аргументы."""
        if event in self.listeners:
            for listener in self.listeners[event]:
                await listener(event, *args)
                
                
class FunEventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, listener):
        """Подписывает слушателя на событие."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    async def emit(self, event, *args, **kwargs):
        """Вызывает слушателей для события."""
        if event in self.listeners:
            for listener in self.listeners[event]:
                await listener(*args, **kwargs)
                
                
CustomEvent = EventManager()
CastomEvent = CustomEvent  # чтоб модули продолжали работать
FunEvent = FunEventManager()
