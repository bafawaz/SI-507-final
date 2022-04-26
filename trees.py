class Teams:
    # parent class for all teams
    def __init__(self, row):
        self.name = row['Team']
        self.fixtures = row['Fixtures']
        self.pts = row['Pts']
        self.rank = row['#']

    def fixtures_info(self):
        if self.fixtures:
            return f"Recent fixures include {self.fixtures}"
        else:
            return f"{self.name} has no recent fixures"

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th." # for the middle of the table (ones with no rank or releg)


class Champs(Teams):
    # subclass for teams that qualify for champions league
    def __init__(self, row):
        super().__init__(row)
        self.champseleg = True

    def info(self):
        if self.rank == 1:
            return f"{self.name} has {self.pts} points and is in {self.rank}st and is elegible for the Champions League."
        elif self.rank == 2:
            return f"{self.name} has {self.pts} points and is in {self.rank}nd and is elegible for the Champions League."
        elif self.rank == 3:
            return f"{self.name} has {self.pts} points and is in {self.rank}rd and is elegible for the Champions League."
        else:
            return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for the Champions League."


class Euro(Teams):
    # subclass for teams that qualify for europa league
    def __init__(self, row):
        super().__init__(row)
        self.euro = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for the Europa League."


class PlayIn(Teams):
    # subclass for teams that qualify for play ins
    def __init__(self, row):
        super().__init__(row)
        self.play_in = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for play-ins."


class Relegation(Teams):
    # subclass for teams that are at risk of relegation
    def __init__(self, row):
        super().__init__(row)
        self.releg = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is in relegation"
