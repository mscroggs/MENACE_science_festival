import sys
import tty
import json
import termios
import tweeter
import plotter

class OutOfBeads(BaseException):
    pass

class Collector(object):
    def __init__(self):
        self.filename = "data-dump/data.json"
        self.data = []
        self.won = False
        self.drawn = False
        self.lost = False
        self.played = False

    def simulate(self):
        import menace
        from menace.bots import MENACE, Good
        from menace.game import Game
        from time import sleep
        p1 = MENACE()
        p2 = Good()
        g = Game(p1,p2)
        N = 0
        while True:
            winner, moves = g.play(return_moves=True)
            if moves[0] == "RESIGN":
                self.tweet("I just ran out of beads in my first move box. Uh oh!")
                raise OutOfBeads
            if moves[0] == 4:
                if moves[1] % 2 == 0:
                    m = "20"
                else:
                    m = "21"
            elif moves[0]%2==0:
                if moves[1] == 4:
                    m = "00"
                elif (moves[0] in [0,8] and moves[1] in [0,8]) or (moves[0] in [2,6] and moves[1] in [2,6]):
                    m = "01"
                elif moves[1] in [0,2,6,8]:
                    m = "03"
                elif abs(moves[0]-moves[1]) in [1,3]:
                    m = "02"
                else:
                    m = "04"
            else:
                if moves[1] == 4:
                    m = "12"
                elif (moves[0] in [1,7] and moves[1] in [1,7]) or (moves[0] in [3,5] and moves[1] in [3,5]):
                    m = "14"
                elif moves[1] in [1,7,3,5]:
                    m = "11"
                elif abs(moves[0]-moves[1] in [1,3]):
                    m = "10"
                else:
                    m = "13"
            if winner == 0:
                w = "1"
            elif winner == 1:
                w = "0"
            else:
                w = "2"
            self.data.append((m,w))
            print(m,w)

            N += 1
            self.crunch_data(N)
            print("Waiting 1 second")
            sleep(1)

    def crunch_data(self, N):
        if N % 1 == 0:
            print("Saving, please wait...")
            self.save()
            print("Plotting, please wait...")
            self.plot()
        if N % 25 == 0:
            self.tweet_graph("This graph shows my learning progress after "+str(N)+" games")
        if not self.won and self.data[-1][1] == "0":
            self.tweet("I just won my first game!")
            self.won = True
        if not self.drawn and self.data[-1][1] == "1":
            self.tweet("I just drew my first game!")
            self.drawn = True
        if not self.lost and self.data[-1][1] == "2":
            self.lost = True
        if not self.played:
            self.tweet("I just played my first game!")
            self.played = True

    def tweet_graph(self, tweet):
        tweeter.send_tweet_with_image(tweet, "display/line.png")

    def tweet(self, tweet):
        print("Tweeting...")
        tweeter.send_tweet(tweet)

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        ext = filename.split(".")[-1]
        if ext == "json":
            with open(filename) as f:
                self.data = json.load(f)
        elif ext == "csv":
            self.data = []
            with open(filename) as f:
                for line in f:
                    self.data.append(line.strip("\n").split(","))
        else:
            raise TypeError("File format ."+ext+" not recognised")

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        ext = filename.split(".")[-1]
        if ext == "json":
            with open(filename,"w") as f:
                json.dump(self.data, f)
        elif ext == "csv":
            with open(filename,"w") as f:
                for line in self.data:
                    f.write(",".join(line)+"\n")
        else:
            print("Filename not recognised, exporting as JSON instead")
            self.save(filename+".json")

    def plot(self):
        plotter.line_plot(self.data,"display/line.png")

    def start(self):
        N = 0
        tty.setcbreak(sys.stdin)
        while True:
            self.collect()
            N += 1
            self.crunch_data(N)

    def end(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        old[3] = old[3] | termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def collect(self):
        c1 = self.prompt_for_moves()
        c2 = self.prompt_for_outcome()
        if self.confirm():
            self.data.append(("".join(c1),c2))
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
        print("Where did MENACE go on its first move?")
        print("PRESS 0 for    PRESS 1 for    PRESS 2 for")
        print("   O| |            |O|            | |    ")
        print("   -+-+-          -+-+-          -+-+-   ")
        print("    | |            | |            |O|    ")
        print("   -+-+-          -+-+-          -+-+-   ")
        print("    | |            | |            | |    ")
        m1 = self.prompt(["0","1","2"])

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
