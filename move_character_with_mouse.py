from pico2d import *
import random


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

def handle_events():
    global running
    global x, y, arrow_x, arrow_y, target_queue
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # 클릭한 위치에 손 화살표 생성
            arrow_x, arrow_y = event.x, TUK_HEIGHT - 1 - event.y
            # 캐릭터의 이동 목표를 클릭한 위치로 설정
            target_queue.append([arrow_x,arrow_y])



def move_character(start_x, start_y, target_x, target_y):
    x, y = start_x, start_y
    frame = 0
    global target_queue
    for i in range(0, 100 + 1, 2):
        clear_canvas()
        TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
        t = i / 100
        x = (1 - t) * start_x + t * target_x
        y = (1 - t) * start_y + t * target_y
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
        frame = (frame + 1) % 8
        for i in target_queue:
            hand.draw(i[0], i[1])
        update_canvas()
        delay(0.02)  # 적절한 딜레이를 주어 움직임이 자연스럽게 보이도록 함


    return x, y



running = True

x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
current_x, current_y = x, y
arrow_x, arrow_y = x, y
target_queue = []



while running:

    handle_events()
    if x == current_x and y == current_y:
        # 캐릭터가 이동 목표에 도달하면 손 화살표 숨기기
        if len(target_queue) == 0: #가야할 길이 비어있으면의 예외처리
            clear_canvas()
            TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
            character.clip_draw(0, 100 * 1, 100, 100, x, y)
            update_canvas()
        else:
            if target_queue[0][0] == x and target_queue[0][1] == y:
                target_queue.pop(0)
            if len(target_queue) != 0:
                current_x, current_y = target_queue[0][0], target_queue[0][1]

        #clear_canvas()
        #TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
        #character.clip_draw(0, 100 * 1, 100, 100, x, y)

    else:
        x, y = move_character(x, y, current_x, current_y)


close_canvas()