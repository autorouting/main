import onevehicleroutegen_web
import multiprocessing
import api_key

def run_function():
    print(onevehicleroutegen_web.main(api_key.google_geocoding_api, open("locations.txt", "r").read())[0].replace("<br>", "\n").replace("<B>", "\n\t").replace("</B>", "\t").replace("<h1>", "\n\t").replace("</h1>", "\t\n").replace("<p style=\"color:Tomato;\">", " ").replace("</p>", "\t\n"))

def createWorkers(n):
    for i in range(n):
        p = multiprocessing.Process(target=run_function, name="Process " + str(i), args=tuple())
        p.start()

if __name__ == "__main__":
    createWorkers(5)