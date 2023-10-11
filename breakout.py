"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from campy.graphics.gobjects import GLabel
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10  # 100 frames per second
NUM_LIVES = 3  # Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES
    game_over_label = GLabel("Game Over")
    # Add the animation loop here!
    while True:
        if graphics.game_started:
            graphics.move_ball()

            if graphics.ball.x <= 0 or graphics.ball.x >= graphics.window.width - graphics.ball.width:
                graphics.set_dx(-graphics.get_dx())  # reverse horizontal direction

            if graphics.ball.y <= 0:
                graphics.set_dy(-graphics.get_dy())  # reverse vertical direction

            if graphics.ball.y >= graphics.window.height:
                lives -= 1
                if lives == 0:
                    print("Game over!")
                    graphics.window.add(game_over_label, x=(graphics.window.width - game_over_label.width) / 2,
                                        y=(graphics.window.height + game_over_label.height) / 2)
                    break
                else:
                    print(f"Lives left: {lives}")
                    graphics.set_ball_position()

            if graphics.bricks_remaining == 0:
                print("Win!")
                break

            graphics.detect_collisions()

        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
