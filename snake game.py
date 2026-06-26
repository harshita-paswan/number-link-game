import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Game Window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tkinter.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT
)
canvas.pack()

# Initialize Game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)

snake_body = []

velocityX = 0
velocityY = 0

game_over = False
score = 0


def change_direction(e):
    global velocityX, velocityY, game_over

    if game_over:
        return

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1

    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1

    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0

    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0


def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return

    # Wall collision
    if (
        snake.x < 0
        or snake.x >= WINDOW_WIDTH
        or snake.y < 0
        or snake.y >= WINDOW_HEIGHT
    ):
        game_over = True
        return

    # Self collision
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Food collision
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))

        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

        score += 1

    # Update body
    for i in range(len(snake_body) - 1, -1, -1):
        if i == 0:
            snake_body[i].x = snake.x
            snake_body[i].y = snake.y
        else:
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    move()

    canvas.delete("all")

    # Food
    canvas.create_rectangle(
        food.x,
        food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="red"
    )

    # Snake Head
    canvas.create_rectangle(
        snake.x,
        snake.y,
        snake.x + TILE_SIZE,
        snake.y + TILE_SIZE,
        fill="lime"
    )

    # Snake Body
    for tile in snake_body:
        canvas.create_rectangle(
            tile.x,
            tile.y,
            tile.x + TILE_SIZE,
            tile.y + TILE_SIZE,
            fill="lime"
        )

    if game_over:
        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            text=f"Game Over! Score: {score}",
            fill="white",
            font=("Arial", 20)
        )
    else:
        canvas.create_text(
            50,
            20,
            text=f"Score: {score}",
            fill="white",
            font=("Arial", 12)
        )

    window.after(100, draw)


window.bind("<KeyPress>", change_direction)

draw()

window.mainloop()