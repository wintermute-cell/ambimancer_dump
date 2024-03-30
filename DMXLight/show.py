import colors
import typedef

def run(fixtures: list[typedef.Fixture]):
    fixtures[0].color(colors.RED)
    fixtures[0].dim(255, 5000)
