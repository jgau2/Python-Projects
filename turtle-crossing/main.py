import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
player = Player()
scoreboard = Scoreboard()
screen.setup(width=600, height=600)
screen.tracer(0)
car_manager = CarManager()

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.generate_car()
    car_manager.move_car()

    screen.listen()
    screen.onkey(player.move, "Up")

    # detect if player crosses road
    if player.ycor() > 280:
        scoreboard.increase_level()
        car_manager.level_up()
        player.reset_player()

    # detect if car hits player and end game
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            scoreboard.game_over()
            game_is_on = False
