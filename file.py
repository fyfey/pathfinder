import glob

class File:

    ASCII_START  = "S"
    ASCII_TARGET = "F"
    ASCII_WALL   = "#"
    ASCII_BLANK  = "."

    def __init__(self):
        self.files = []

    def setGrid(self, grid):
        self.grid = grid

    def load(self):
        self.files = glob.glob('./*.map')
        i = 1
        for file in self.files:
            print("%d) %s" % (i, file))
            i += 1
        if not self.files:
            print("No maps found!")
            return False
        while True:
            try:
                number = int(input("Enter a number (0 to cancel): "))
                number -= 1
                if number == -1:
                    print("Load cancelled")
                    return False
                filename = self.files[int(number)]
                break
            except (IndexError, ValueError):
                print("Please enter a valid entry")
        f = open(filename, 'r')
        grid = []
        for line in f:
            a_line = []
            for i in range(0, len(line)-1):
                a_line.append(line[i])
            grid.append(a_line)
        return (list(reversed(grid)))

    def save(self):
        name = input("Enter a map name: ")
        export = ""
        for i in range(self.grid.height, 0, -1):
            for j in range(1, self.grid.width + 1):
                cell = self.grid.cell(j, i)
                export += self.getAscii(cell)
            export += "\n"
        f = open("%s.map" % name, 'w')
        f.write(export)
        print("Saved map - %s.map" % name)

    def getAscii(self, cell):
        if cell.start:
            char = self.ASCII_START
        elif cell.wall:
            char = self.ASCII_WALL
        elif cell.target:
            char = self.ASCII_TARGET
        else:
            char = self.ASCII_BLANK

        return char
