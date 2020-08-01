class HelloWorld:
    def __init__(self):
        self.message = "Hello world! We made some changes"

    def __str__(self):
        return self.message

if __name__ == "__main__":
    myMessage = HelloWorld()
    print(myMessage)
