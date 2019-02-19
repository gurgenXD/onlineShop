class DandP(object):
    def __init__(self, request):
        self.session = request.session
        dandp = self.session.get('dandp')
        if not dandp:
            dandp = self.session['dandp'] = {
                'delivery': 0,
                'payment': 0,
            }
        self.dandp = dandp
    
    def save(self):
        self.session['dandp'] = self.dandp
        self.session.modified = True
    
    def update(self, delivery, payment):
        self.dandp['payment'] = payment
        self.dandp['delivery'] = delivery
        self.save()
    
    def clear(self):
        self.dandp['payment'] = 0
        self.dandp['delivery'] = 0
        self.session.modified = True
