"""Run with Python and a Tk display; each exit path gets a fresh interpreter."""
import subprocess
import sys
from pathlib import Path
from turtle import Screen
from main import Pong


def run(exit_path):
    screen = Screen()
    game = Pong(screen)
    canvas = screen.getcanvas()
    game.window.update()
    canvas.focus_force()
    game.window.update()
    target = game.window.focus_get()
    assert target is not None and target.winfo_class() == "Canvas", "Tk needs a display and keyboard focus"
    def key(name):
        for event in ("KeyPress", "KeyRelease"):
            if name in ("s", "w") and sys.platform == "win32":
                target.event_generate("<" + event + ">", keycode=ord(name.upper()))
            else:
                target.event_generate("<" + event + "-" + name + ">")
        if game.playing:
            game.window.update()
    assert (game.score.l_score, game.score.r_score) == (0, 0)
    key("w"); key("Down")
    assert (game.left.ycor(), game.right.ycor()) == (20, -20)
    key("s"); key("Up")
    assert (game.left.ycor(), game.right.ycor()) == (0, 0)
    ball = game.ball
    for y, sign in ((279, 1), (-279, -1)):
        ball.goto(0, y); ball.y_move = sign * 10
        game.advance()
        assert ball.y_move == -sign * 10
    for x, sign in ((320, 1), (-320, -1)):
        ball.goto(x, 0); ball.x_move = sign * 10
        speed = ball.move_speed
        game.advance()
        assert ball.x_move == -sign * 10 and ball.move_speed < speed
        game.advance()
        assert ball.x_move == -sign * 10
    for x, sign, score in ((380, 1, (1, 0)), (-380, -1, (1, 1))):
        ball.goto(x, 100); ball.x_move = sign * 10
        game.advance()
        assert tuple(ball.pos()) == (0, 0) and ball.move_speed == 0.1
        game.advance()
        assert (game.score.l_score, game.score.r_score) == score
    game.tick()
    assert game.timer is not None
    if exit_path == "escape":
        key("Escape")
    else:
        game.window.tk.call(game.window.protocol("WM_DELETE_WINDOW"))
    assert not game.playing and game.timer is None
    print(exit_path + ": keys, wall/paddle rebounds, two points, fresh serve and clean exit OK")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        for mode in ("escape", "window"):
            subprocess.run([sys.executable, str(Path(__file__).resolve()), mode], check=True)
