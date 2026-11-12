from turtle import Screen, Terminator
from tkinter import TclError
import sys

from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard


class Pong:
    """One two-player match, driven by the Tk event loop."""

    def __init__(self, screen):
        self.screen = screen
        screen.bgcolor("black")
        screen.setup(width=800, height=600)
        screen.title("Pong | W/S and arrows | Esc to quit")
        screen.tracer(0)
        self.right = Paddle((350, 0))
        self.left = Paddle((-350, 0))
        self.ball = Ball()
        self.score = Scoreboard()
        self.playing = True
        self.timer = None
        self.window = screen.getcanvas().winfo_toplevel()
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        for key, action in (("Up", self.right.go_up), ("Down", self.right.go_down), ("Escape", self.close)):
            screen.onkey(action, key)
        # Windows virtual keys preserve the W/S positions with a non-Latin input layout.
        def move_left(event):
            key = event.keysym.lower()
            if key == "w" or (sys.platform == "win32" and event.keycode == 87):
                self.left.go_up()
            elif key == "s" or (sys.platform == "win32" and event.keycode == 83):
                self.left.go_down()
        screen.getcanvas().bind("<KeyRelease>", move_left, add="+")
        screen.listen()

    def advance(self):
        ball = self.ball
        ball.move()
        if (ball.ycor() > 280 and ball.y_move > 0) or (ball.ycor() < -280 and ball.y_move < 0):
            ball.bounce_y()
        if ((ball.x_move > 0 and 320 < ball.xcor() < 350 and ball.distance(self.right) < 50)
                or (ball.x_move < 0 and -350 < ball.xcor() < -320 and ball.distance(self.left) < 50)):
            ball.bounce_x()
        if ball.xcor() > 380:
            self.score.l_point()
            ball.reset_position()
        elif ball.xcor() < -380:
            self.score.r_point()
            ball.reset_position()

    def tick(self):
        self.timer = None
        if not self.playing:
            return
        try:
            self.advance()
            self.screen.update()
        except (Terminator, TclError):
            if self.playing:
                raise
        if self.playing:
            self.timer = self.window.after(max(1, round(self.ball.move_speed * 1000)), self.tick)

    def close(self):
        if not self.playing:
            return
        self.playing = False
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None
        self.screen.bye()


if __name__ == "__main__":
    screen = Screen()
    game = Pong(screen)
    game.tick()
    if game.playing:
        screen.mainloop()
