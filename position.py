class Position:
    '''
    This class is used to store all the data used to create orders and to make the calculation.
    '''
    def __init__(self):
        self.open_price=0.0
        self.highest_price=0.0
        self.lowest_price=0.0
        self.status='close'
        self.symbol=''
        self.number=0
        self.close_mode=''
        self.current_price=0.0
        self.number_lost=0
        self.total_yield = 1.0
        self.close_price=0.0
        self.time=0
        self.effective_yield=0
        self.highest_yield = 1
        self.stop_loss = False
        self.back_testing = False
        self.start_time = 0
        self.period = 14