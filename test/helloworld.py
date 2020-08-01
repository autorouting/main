class HelloWorld:
    def __init__(self):
        self.message = "Hello world!"

    def __str__(self):
        return self.message

if __name__ == "__main__":
    myMessage = HelloWorld()
    print(myMessage)
