"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # initialize paddle attributes
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_offset = PADDLE_OFFSET  # initialize paddle_offset

        self.ball_radius = ball_radius

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = "black"
        self.window.add(self.paddle, x=(self.window.width - self.paddle.width) / 2,
                        y=(self.window.height - self.paddle_offset))

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width - self.ball_radius) / 2,
                        y=(self.window.height - self.ball_radius) / 2)
        # Default initial velocity for the ball
        self.__dx = 0  # change to private variable
        self.__dy = 0  # change to private variable
        # initialize mouse click
        self.game_started = False
        # Initialize our mouse listeners
        onmousemoved(self.paddle_move)  # 當滑鼠移動時，呼叫 self.paddle_move 函式
        onmouseclicked(self.mouse_click)  # 當滑鼠點擊時，呼叫 self.mouse_click 函式
        # Draw bricks
        self.draw_bricks()
        # number of bricks
        self.bricks_remaining = BRICK_ROWS * BRICK_COLS
        # create ball and initialize velocity/position
        self.set_ball_position()

    def draw_bricks(self):
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                # calculate the x and y positions for each brick
                x = col * (BRICK_WIDTH + BRICK_SPACING)
                y = BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)

                # create a brick at the calculated position
                brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                brick.filled = True

                # add brick color based on row
                if row < (BRICK_ROWS / 5):
                    brick.fill_color = 'red'
                elif row < 2 * (BRICK_ROWS / 5):
                    brick.fill_color = 'orange'
                elif row < 3 * (BRICK_ROWS / 5):
                    brick.fill_color = 'yellow'
                elif row < 4 * (BRICK_ROWS / 5):
                    brick.fill_color = 'green'
                else:
                    brick.fill_color = 'blue'

                # add the brick to the window
                self.window.add(brick, x, y)

    def paddle_move(self, event):
        new_x = (event.x - self.paddle_width / 2)
        # ensure the paddle stays within the window boundaries
        if new_x < 0:
            new_x = 0
        elif new_x > self.window.width - self.paddle.width:
            new_x = self.window.width - self.paddle.width
        # update the paddle's position
        self.paddle.x = new_x

    def set_ball_position(self):  # put ball in the middle of the window
        self.__dx = 0
        self.__dy = 0
        self.game_started = False
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2

    def mouse_click(self, event):
        if not self.game_started:
            self.game_started = True
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def set_dx(self, dx):  # set the horizontal velocity of the ball
        self.__dx = dx

    def get_dx(self):  # get the horizontal velocity of the ball
        return self.__dx

    def set_dy(self, dy):  # set the vertical velocity of the ball
        self.__dy = dy

    def get_dy(self):  # get the vertical velocity of the ball
        return self.__dy

    def move_ball(self):
        self.ball.move(self.__dx, self.__dy)

    def detect_collisions(self):  # Ball's four corner coordinates
        ball_points = [(self.ball.x, self.ball.y),
                       (self.ball.x + 2 * BALL_RADIUS, self.ball.y),
                       (self.ball.x, self.ball.y + 2 * BALL_RADIUS),
                       (self.ball.x + 2 * BALL_RADIUS, self.ball.y + 2 * BALL_RADIUS)]
        collision_detected = False
        # check each corner of the ball
        for point in ball_points:
            x, y = point
            obj = self.window.get_object_at(x, y)
            if obj is not None:
                collision_detected = True
                # if collide with the paddle, bounce back
                if obj == self.paddle:
                    self.__dy = -abs(self.__dy)
                else:
                    # if collide with the brick, bounce back and remove the brick
                    self.__dy = -self.__dy
                    self.window.remove(obj)
                    self.bricks_remaining -= 1
                break  # no need to check other corners

        # If no collision at any corner, ball continues in its original direction
        if not collision_detected:
            pass
