import sys
import tty
import json
import termios
import tweeter
import plotter
from random import choice

class OutOfBeads(BaseException):
    pass

class Collector(object):
    def __init__(self, data=None, tweet=True, where="my current location", hashtag="#MENACE"):
        self.filename = "data-dump/data.json"
        self.data = []
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.played = 0
        if data is not None:
            if data.split(".")[-1] != "json":
                raise TypeError("Can only load state from json")
            self.load_json(data)
        self.TWEETING = tweet
        self.where = where
        self.hashtag = hashtag
        self.plot_etc()

    def simulate(self):
        import menace
        from menace.bots import MENACE, Good, QuiteGood
        from menace.game import Game
        from time import sleep
        from random import randrange
        p1 = MENACE()
        p2 = QuiteGood()
        g = Game(p1,p2)
        while True:
            winner, moves = g.play(return_moves=True)
            if moves[0] == "RESIGN":
                self.tweet("I just ran out of beads in my first move box. Please come reset me, @mscroggs!")
                raise OutOfBeads
            if winner == 0:
                w = "1"
            elif winner == 1:
                w = "0"
            else:
                w = "2"
            self.data.append(w)
            print(w)

            self.crunch_data()
            print("Waiting 1 second")
            sleep(1)

    def crunch_data(self):
        if self.played == 0:
            s2 = ""
            if self.data[-1] == "0":
                s2 = " And I've already won a game!"
            if self.data[-1] == "1":
                s2 = " I drew. Come along and see if you can beat me!"
            if self.data[-1] == "2":
                s2 = " I lost, but I going to learn from my mistakes..."
            self.tweet("I just played today's first game of Noughts & Crosses at "+self.where+"."+s2+" "+self.hashtag)
        self.played += 1
        if self.data[-1] == "0":
            if self.played != 1:
                if self.won == 0:
                    self.tweet("I just won a game of Noughts & Crosses for the first time. Not bad for a pile of matchboxes! "+self.hashtag)
                else:
                    nth = str(self.won)
                    if nth[-1]=="1" and nth[-2:]!="11":
                        nth += "st"
                    elif nth[-1]=="2" and nth[-2:]!="12":
                        nth += "nd"
                    else:
                        nth += "th"
                    self.tweet(choice(["I won another game of Noughts & Crosses!",
                                       "I just won a game. Take that, humans!",
                                       "Breaking news: A human just lost a game of Noughts & Crosses to a pile of matchboxes.",
                                       "I've just won my "+nth+" game of Noughts & Crosses of the day.",
                                       "I have become sentient enough to win another game of Noughts & Crosses.",
                                       "I have now won "+str(self.won)+" games of Noughts & Crosses. I'm nearly ready to take over the world.",
                                       "MENACE wins again!"
                                      ])+" "+self.hashtag)
            self.won += 1
        if self.data[-1] == "1":
            if self.drawn == 0 and self.played != 1:
                self.tweet("I just drew a game of Noughts & Crosses for the first time. "+self.hashtag)
            self.drawn += 1
        if self.data[-1] == "2":
            self.lost += 1
        if self.played%20 == 0:
            self.plot_etc(N=self.played)
        if self.played%20 == 10:
            self.plot_etc(N2=(self.won,self.drawn,self.lost))
        else:
            self.plot_etc()

    def plot_etc(self, N=None, N2=None):
        print("Saving, please wait...")
        self.save()
        print("Plotting, please wait...")
        self.plot()
        print("Saving totals, please wait...")
        self.output_numbers()
        if N is not None:
            self.save(N=N)
            self.tweet_graph("This graph shows my learning progress after "+str(N)+" games. "+self.hashtag)
        if N2 is not None:
            self.tweet_graph("I've played "+str(self.played)+" games so far today: I've won "+str(N2[0])+", drawn "+str(N2[1])+", and lost "+str(N2[2])+". "+self.hashtag)

    def output_numbers(self):
        with open("display/numbers.txt","w") as f:
            f.write(str(self.won)+","+str(self.drawn)+","+str(self.lost))

    def tweet_graph(self, tweet):
        if self.TWEETING:
            print("Tweeting \""+tweet+"\"...")
            tweeter.send_tweet_with_image(tweet, "display/line.png")
        else:
            print("Normally I would tweet \""+tweet+"\" and a graph but tweeting is disabled...")

    def tweet(self, tweet):
        if self.TWEETING:
            print("Tweeting \""+tweet+"\"...")
            tweeter.send_tweet(tweet)
        else:
            print("Normally I would tweet \""+tweet+"\" but tweeting is disabled...")

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        ext = filename.split(".")[-1]
        if ext == "json":
            self.load_json(filename)
        elif ext == "csv":
            self.data = []
            with open(filename) as f:
                for line in f:
                    self.data.append(line.strip("\n"))
        else:
            raise TypeError("File format ."+ext+" not recognised")

    def save_json(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename,"w") as f:
            json.dump({"data":self.data,"w":self.won,"l":self.lost,"d":self.drawn,"p":self.played}, f)

    def load_json(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename) as f:
            temp = json.load(f)
        self.data = temp["data"]
        self.won = temp["w"]
        self.lost = temp["l"]
        self.drawn = temp["d"]
        self.played = temp["p"]


    def save(self, filename=None, N=None):
        if filename is None:
            filename = self.filename
        ext = filename.split(".")[-1]
        if N is not None:
            fs = filename.split(".")
            filename = ".".join(fs[:-1])+"-"+str(N)+"."+fs[-1]
        if ext == "json":
            self.save_json(filename)
        elif ext == "csv":
            with open(filename,"w") as f:
                f.write("\n".join(self.data))
        else:
            print("Filename not recognised, exporting as JSON instead")
            self.save(filename+".json")

    def plot(self):
        plotter.line_plot(self.data,"display/line.png")

    def start(self):
        tty.setcbreak(sys.stdin)
        while True:
            self.collect()
            self.crunch_data()

    def end(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        old[3] = old[3] | termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def collect(self):
        c2 = self.prompt_for_outcome()
        if self.confirm():
            self.data.append(c2)
        else:
            self.collect()

    def confirm(self):
        return True

    def prompt_for_moves(self):
        for i in range(5):
            print("")
        print("-"*30)
        for i in range(5):
            print("")
        for i in range(2):
            print("")
        print("Where did the opponent go next?")
        if m1 == "0":
            print("PRESS 0 for    PRESS 1 for    PRESS 2 for    PRESS 3 for    PRESS 4 for    ")
            print("   O| |           O| |           O|X|           O| |X          O| |        ")
            print("   -+-+-          -+-+-          -+-+-          -+-+-          -+-+-       ")
            print("    |X|            | |            | |            | |            | |X       ")
            print("   -+-+-          -+-+-          -+-+-          -+-+-          -+-+-       ")
            print("    | |            | |X           | |            | |            | |        ")
            return m1,self.prompt(["0","1","2","3","4"])
        if m1 == "1":
            print("PRESS 0 for    PRESS 1 for    PRESS 2 for    PRESS 3 for    PRESS 4 for    ")
            print("   X|O|            |O|            |O|            |O|            |O|        ")
            print("   -+-+-          -+-+-          -+-+-          -+-+-          -+-+-       ")
            print("    | |           X| |            |X|            | |            | |        ")
            print("   -+-+-          -+-+-          -+-+-          -+-+-          -+-+-       ")
            print("    | |            | |            | |           X| |            |X|        ")
            return m1,self.prompt(["0","1","2","3","4"])
        if m1 == "2":
            print("PRESS 0 for    PRESS 1 for    ")
            print("    | |            | |        ")
            print("   -+-+-          -+-+-       ")
            print("    |O|            |O|        ")
            print("   -+-+-          -+-+-       ")
            print("    |X|            | |X       ")
            return m1,self.prompt(["0","1"])


    def prompt_for_outcome(self):
        for i in range(2):
            print("")
        print("PRESS 0 if MENACE won    PRESS 1 if draw    PRESS 2 if MENACE lost")
        return self.prompt(["0","1","2"])

    def prompt(self, allow = None):
        char = sys.stdin.read(1)
        if allow is not None:
            while char not in allow:
                print("ERROR, please try again")
                char = sys.stdin.read(1)
        return char
