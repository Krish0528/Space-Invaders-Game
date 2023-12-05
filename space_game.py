import turtle
import math
import random

# Set up the game window screen
window = turtle.Screen()
window.bgcolor("green")
window.title("Space Invaders game made by ABK for Follow tuts")
window.bgpic("background.gif")

# Register the shape
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
# player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

player_speed = 15

# Choose a number of enemies
number_of_enemies = 10
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    # enemy.color("Red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemy_speed = 5

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bullet_speed = 30

# define bullet state
# ready - ready to fire
# fire - bullet is firing
bullet_state = "ready"


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bullet_state as a global if it needs changed
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


# For collision between enemy and bullet
def is_collision_enemy_bullet(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 25:
        return True
    else:
        return False


# For collision between enemy and player
def is_collision_enemy_player(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 30:
        return True
    else:
        return False


# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main game loop
game_over = False
missed_enemies = 0
while True:

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and game_over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 5:
                        game_over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            # Change enemy direction
            enemy_speed *= -1

        if enemy.xcor() < -270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and game_over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 5:
                        game_over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            # Change enemy direction
            enemy_speed *= -1

        # check for a collision between the bullet and the enemy
        if is_collision_enemy_bullet(bullet, enemy):
            # Reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            enemy_speed += 0.5
            # update the score
            score += 10
            score_string = "Score: %s" % score
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
        # check for a collision between the player and enemy
        if is_collision_enemy_player(player, enemy):
            game_over = True
            if game_over:
                player.hideturtle()
                bullet.hideturtle()
                for e in enemies:
                    e.hideturtle()
                window.bgpic("end.gif")
                break

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"
        
turtle.done()
