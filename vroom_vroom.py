import pygame
import random
import math

# window dimensions
win_x = 600
win_y = 600

fps = 30

# colors
black = pygame.Color(0, 0, 0)
gray1 = pygame.Color(90, 90, 90)
gray2 = pygame.Color(150, 150, 150)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0, 255)
red = pygame.Color(255, 0, 0)
yellow = pygame.Color(255, 255, 0)

pygame.init()

pygame.display.set_caption('Simulation')
sim_window = pygame.display.set_mode((win_x, win_y))

clock = pygame.time.Clock()

# infrastructure size
sidewalk_width = 5
road_width = 35
car_size = 15
guy_size = 3
house_size = 20

# rectangles
car = pygame.Rect(0, 0, car_size, car_size)

intersection = pygame.Rect(0, 0, road_width, road_width)

roadV = [pygame.Rect(0, (win_y + road_width)//2, road_width, (win_y - road_width)//2),
         pygame.Rect(0, 0, road_width, (win_y - road_width)//2)]

roadH = [pygame.Rect((win_x + road_width)//2, 0, (win_y - road_width)//2, road_width),
         pygame.Rect(0, 0, (win_y - road_width)//2, road_width)]

roads = [roadH, roadV]

post_office = pygame.Rect(20, 50, 50, 50)
post_road = pygame.Rect(80, 70, road_width, (win_y - road_width)//2 - 70)

# adjustments
intersection.center = (win_x // 2, win_y // 2)
car.center = intersection.center

for road in roadV:
    road.centerx = intersection.centerx
for road in roadH:
    road.centery = intersection.centery

# houses
houses = [pygame.Rect(roadV[0].x - (house_size + sidewalk_width), 10, house_size, house_size),
          pygame.Rect(roadV[0].x - (house_size + sidewalk_width), 80, house_size, house_size),
          pygame.Rect(roadV[0].x - (house_size + sidewalk_width), 160, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), 100, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), 150, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), 250, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), 40, house_size, house_size),
          pygame.Rect(190, roadH[0].y - (house_size + sidewalk_width), house_size, house_size),
          pygame.Rect(20, roadH[0].y + (road_width + sidewalk_width), house_size, house_size),
          pygame.Rect(140, roadH[0].y + (road_width + sidewalk_width), house_size, house_size),
          pygame.Rect(210, roadH[0].y + (road_width + sidewalk_width), house_size, house_size),
          pygame.Rect(roadV[0].x - (house_size + sidewalk_width), win_y // 2 + 50, house_size, house_size),
          pygame.Rect(roadV[0].x - (house_size + sidewalk_width), win_y // 2 + 80, house_size, house_size),
          pygame.Rect(roadV[0].x - (house_size + sidewalk_width), win_y // 2 + 190, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), win_y // 2 + 40, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), win_y // 2 + 70, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), win_y // 2 + 110, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), win_y // 2 + 180, house_size, house_size),
          pygame.Rect(roadV[0].x + (road_width + sidewalk_width), win_y // 2 + 270, house_size, house_size),
          pygame.Rect(win_x // 2 + 100, roadH[0].y - (house_size + sidewalk_width), house_size, house_size),
          pygame.Rect(win_x // 2 + 130, roadH[0].y - (house_size + sidewalk_width), house_size, house_size),
          pygame.Rect(win_x // 2 + 220, roadH[0].y - (house_size + sidewalk_width), house_size, house_size),
          pygame.Rect(win_x // 2 + 260, roadH[0].y - (house_size + sidewalk_width), house_size, house_size),
          ]

house_num = len(houses)
house_active_chance = list()  # in percentage(%)
for chance in range(house_num):
    house_active_chance.append(random.randint(1, 10))

house_active = [False] * house_num
house_CD = fps * 20
house_cooldown = [house_CD] * house_num

# guy
mailman = car.center
guy_path = list()
guy_speed = 2
guy_in_car = True
guy_work = False
guy_at_loc = True

# car
car_path = list()
car_speed = 10
car_at_loc = True

# mechanics
counter = 1

def track_building(mouse_pos, type):
    pointer = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

    buildingType = "NA"
    for (i, house) in enumerate(houses):
        if pygame.Rect.colliderect(pointer, house):
            buildingType = "house"
            house_num = i

    if buildingType == "NA":
        if pygame.Rect.colliderect(pointer, post_office):
            buildingType = "post"

    if buildingType == "NA":
        return ("Error", -1)

    if type == "road":
        if buildingType == "house":
            min_dis = win_x + win_y

            for (i, ver) in enumerate(roadV):
                x = abs(ver.centerx - houses[house_num].centerx)
                if x < min_dis:
                    min_dis = x
                    nearest_road = ("verRoad", i, ver.centerx, houses[house_num].centery)

            for (i, hor) in enumerate(roadH):
                y = abs(hor.centery - houses[house_num].centery)
                if y < min_dis:
                    min_dis = y
                    nearest_road = ("horRoad", i, houses[house_num].centerx, hor.centery)

            return nearest_road
        elif buildingType == "post":
            return ("postRoad", -1, post_road.centerx, post_office.centery + 10)

    elif type == "building":
        if buildingType == "house":
            return (buildingType, house_num)
        elif buildingType == "post":
            return (buildingType, -1)

def check_click(mouse_pos):
    pointer = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

    for (i, house) in enumerate(houses):
        if pygame.Rect.colliderect(pointer, house):
            return "house", i

    for (i, ver) in enumerate(roadV):
        if pygame.Rect.colliderect(pointer, ver):
            return "verRoad", i

    for (i, hor) in enumerate(roadH):
        if pygame.Rect.colliderect(pointer, hor):
            return "horRoad", i

    if pygame.Rect.colliderect(pointer, post_road):
        return "postRoad", -1

    if pygame.Rect.colliderect(pointer, post_office):
        return "postOffice", -1

    if pygame.Rect.colliderect(pointer, intersection):
        return "intersection", -1

    return "Error", -1

def check_car_pos():
    for (i, ver) in enumerate(roadV):
        if pygame.Rect.colliderect(car, ver):
            return "verRoad", i

    for (i, hor) in enumerate(roadH):
        if pygame.Rect.colliderect(car, hor):
            return "horRoad", i

    if pygame.Rect.colliderect(car, post_road):
        return "postRoad", -1

    if pygame.Rect.colliderect(car, intersection):
        return "intersection", -1

    return "Error", -1

def entity_movement(entity, target, pos = (-1, -1)):
    if entity == "car":
        if car.centerx < target[0]:
            if car.centerx + car_speed > target[0]:
                car.centerx = target[0]
            else:
                car.centerx += car_speed
        elif car.centerx > target[0]:
            if car.centerx - car_speed < target[0]:
                car.centerx = target[0]
            else:
                car.centerx -= car_speed

        if car.centery < target[1]:
            if car.centery + car_speed > target[1]:
                car.centery = target[1]
            else:
                car.centery += car_speed
        elif car.centery > target[1]:
            if car.centery - car_speed < target[1]:
                car.centery = target[1]
            else:
                car.centery -= car_speed
    elif entity == "mailman":
        x, y = pos

        if x < target[0]:
            if x + guy_speed > target[0]:
                x = target[0]
            else:
                x += guy_speed
        elif x > target[0]:
            if x - guy_speed < target[0]:
                x = target[0]
            else:
                x -= guy_speed

        if y < target[1]:
            if y + guy_speed > target[1]:
                y = target[1]
            else:
                y += guy_speed
        elif y > target[1]:
            if y - guy_speed < target[1]:
                y = target[1]
            else:
                y -= guy_speed

        return (x, y)

def create_path_car(track_id, car_id):
    if track_id[0] in ["verRoad", "horRoad"]:
        if car_id[0] != "postRoad":
            if car_id[0] == track_id[0]:
                car_path.append((track_id[2], track_id[3]))
            else:
                car_path.append(intersection.center)
                car_path.append((track_id[2], track_id[3]))
        else:
            if track_id[0] == "horRoad":
                car_path.append((post_road.centerx, win_y // 2))
                car_path.append((track_id[2], track_id[3]))
            elif track_id[0] == "verRoad":
                car_path.append((post_road.centerx, win_y // 2))
                car_path.append(intersection.center)
                car_path.append((track_id[2], track_id[3]))

        return False
    elif track_id[0] == "postRoad":
        if car_id[0] == "postRoad":
            car_path.append((track_id[2], track_id[3]))
        elif car_id[0] == "horRoad":
            car_path.append((track_id[2], win_y // 2))
            car_path.append((track_id[2], track_id[3]))
        else:
            car_path.append(intersection.center)
            car_path.append((track_id[2], win_y // 2))
            car_path.append((track_id[2], track_id[3]))
        return False
    else:
        return True

def create_path_guy(track_id):
    if track_id[0] == "house":
        guy_path.append(houses[track_id[1]].center)
        return False
    elif track_id[0] == "post":
        guy_path.append((post_office.centerx + 10, post_office.centery + 10))
        return False
    else:
        return True

def activate_house():

    for (i, active) in enumerate(house_active):
        if active:
            continue
        else:
            score = random.randint(1, 100)
            if score <= house_active_chance[i] and house_cooldown[i] == house_CD:
                house_active[i] = True
                break

def deactivate_house(pos):
    for (i, house) in enumerate(houses):
        if house.center == pos:
            house_cooldown[i] = 0
            house_active[i] = False
            break

def house_rest():
    for CD in range(house_num):
        if house_cooldown[CD] != house_CD:
            house_cooldown[CD] += 1

while True:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP and car_at_loc and guy_at_loc:
            mouse_pos = pygame.mouse.get_pos()
            car_at_loc = create_path_car(track_building(mouse_pos, "road"), check_car_pos())
            guy_at_loc = create_path_guy(track_building(mouse_pos, "building"))




    # actual stuff
    if car_at_loc and guy_at_loc:
        minDis = win_x + win_y
        minInd = -1
        for (i, active) in enumerate(house_active):
            if active and math.sqrt((houses[i].centerx - car.centerx)**2 + (houses[i].centery - car.centery)**2) < minDis:
                minDis = math.sqrt((houses[i].centerx - car.centerx)**2 + (houses[i].centery - car.centery)**2)
                minInd = i

        if minInd != -1:
            car_at_loc = create_path_car(track_building(houses[minInd].center, "road"), check_car_pos())
            guy_at_loc = create_path_guy(track_building(houses[minInd].center, "building"))


    elif car_at_loc:
        mailman = entity_movement("mailman", guy_path[0], mailman)

        if mailman == guy_path[0]:
            guy_path.pop(0)
            if len(guy_path) == 1:
                deactivate_house(mailman)

        if len(guy_path) == 0:
            guy_at_loc = True
    else:
        entity_movement("car", car_path[0])
        mailman = car.center

        if car.center == car_path[0]:
            car_path.pop(0)

        if len(car_path) == 0:
            guy_path.append(car.center)
            car_at_loc = True

    house_rest()

    if counter == fps:
        activate_house()
        counter = 1
    else:
        counter += 1

    # draw
    sim_window.fill(black)

    for hor_ver in roads:
        for road in hor_ver:
            pygame.draw.rect(sim_window, gray1, road)

    pygame.draw.rect(sim_window, gray2, intersection)

    for (i, house) in enumerate(houses):
        if house_active[i]:
            pygame.draw.rect(sim_window, yellow, house)
        else:
            pygame.draw.rect(sim_window, gray2, house)

    pygame.draw.rect(sim_window, red, post_office)
    pygame.draw.rect(sim_window, gray1, post_road)

    pygame.draw.rect(sim_window, white, car)
    pygame.draw.circle(sim_window, blue, mailman, guy_size)

    pygame.display.update()
    clock.tick(fps)