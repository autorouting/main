class ByeWorld:
    def __init__(self):
        self.message = "Bye world!"

    def __str__(self):
        return self.message

if __name__ == "__main__":
    myMessage = ByeWorld()
    print(myMessage)
