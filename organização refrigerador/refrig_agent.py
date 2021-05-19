import collections
from random import randint

class RefrigAgent:
    refrigerator = []

    def __init__(self):
        for i in range(0,10):
            # fill fridge with 'boxes' that have random expiry date
            best_before = randint(30,180)
            print('Box obtained. It expires in', best_before, 'days.')
            self.refrigerator.append(best_before)
        
        print('Initial box order:', self.refrigerator)
        print('\nSorting boxes...\n')
        self.refrigerator = sorted(self.refrigerator)

        print('Opening refrigerator...\n')
        print('Storing boxes in order of expiry date...')

        print('Refrigerator is now sorted:', self.refrigerator)
        print('\nClosing refrigerator...\n')

        while self.refrigerator:
            box = self.refrigerator.pop(0)
            print('Opening refrigerator...')
            print('Box used had', box, 'days left.')
            print('Closing refrigerator...\n')

refrig_agent_1 = RefrigAgent()