class Consumer():

    inbox = []

    def consume(self, providerName, data):
        print("Data received from provider %s:" % providerName)
        print(data)

    def collect(self, providerName, item):
        self.inbox.append(item)

    def inbox_status(self):
        print("Inbox status... %d items to be processed!" % len(self.inbox))
    
    def output_inbox(self):
        print(self.inbox)