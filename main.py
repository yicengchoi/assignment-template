import pygame
import random
import speech_recognition as sr
import time
import threading

pygame.init()

# color RGB
COLORS = {
    'red': (210, 89, 98),
    'green': (162, 205, 97),
    'blue': (128, 175, 237),
    'yellow': (250, 206, 70),
    'purple': (160, 136, 250),
    'black': (20, 17, 31),
}

#
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Concentration and Reaction Games")

# font
font = pygame.font.SysFont(None, 75)
small_font = pygame.font.SysFont(None, 40)

# game variable
game_running = False
score = 0
current_word, current_color = '', ''
start_time = 0
time_limit = 60  # limited 60s for each round
speech_result = None  # 存储语音识别结果
stop_speech_thread = False  # 控制语音识别
game_over = False  # 标记结束
word_scroll_speed = 9  ### scrolling speed

# button
def button_animation(button, color, text, scale):
    new_button = pygame.Rect(button.x, button.y, button.width * scale, button.height * scale)
    pygame.draw.rect(screen, color, new_button, border_radius=15)  # 按钮为圆角矩形
    text_rect = text.get_rect(center=new_button.center)
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(0.1)  # pause

# 选择一个不同于文字含义的颜色
def get_random_color_and_word():
    word, text_color = random.choice(list(COLORS.items()))  # randomness
    available_colors = [color for name, color in COLORS.items() if name != word]
    display_color = random.choice(available_colors)  # 确保颜色与单词不同
    return word, display_color

def draw_text(word, color, screen, position):
    text = font.render(word, True, color)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)# words

def draw_score(score, screen):
    score_text = small_font.render(f"Score: {score}", True, (20, 17, 31))
    screen.blit(score_text, (20, 20))# score

def draw_time_remaining(remaining_time, screen):
    time_text = small_font.render(f"Time: {remaining_time}s", True, (20, 17, 31))
    screen.blit(time_text, (SCREEN_WIDTH - 200, 20))# time

def draw_rules(screen):
    rules_text = small_font.render("ONLY SAY THE COLOR, NOT THE WORD", True, (20, 17, 31))
    screen.blit(rules_text, (SCREEN_WIDTH // 2 - 360, SCREEN_HEIGHT // 2 - 100))# rule

# 语音识别
def recognize_speech():
    global speech_result, stop_speech_thread
    recognizer = sr.Recognizer()

    while not stop_speech_thread:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Name the colours please...")
            audio = recognizer.listen(source)

            try:
                speech_result = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"Your answer: {speech_result}")
            except sr.UnknownValueError:
                print("Unrecognised, please try again.")
            except sr.RequestError:
                print("Request Error.")

# 倒计时显示
def countdown(screen):
    for i in range(3, 0, -1):
        screen.fill((250, 228, 217))  # 背景
        countdown_text = font.render(str(i), True, (20, 17, 31))
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)  # 延迟1秒

    # 显示 "Go!" 并延迟一秒
    screen.fill((250, 228, 217))  # 背景
    go_text = font.render("Go!", True, (20, 17, 31))
    screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - go_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1000)

# 开始游戏
def start_game():
    global game_running, score, current_word, current_color, start_time, stop_speech_thread, game_over
    game_running = True
    score = 0
    stop_speech_thread = False
    current_word, current_color = get_random_color_and_word()
    game_over = False

    # 倒计时过程
    countdown(screen)
    
    # 游戏开始
    start_time = time.time()  # 记录开始时间
    threading.Thread(target=recognize_speech).start()  # 启动语音识别线程

# 结束游戏
def end_game():
    global game_running, stop_speech_thread, game_over
    game_running = False
    stop_speech_thread = True
    game_over = True
    print(f"Game over! Final score. {score}")

# 主循环
def game_loop():
    global current_word, current_color, score, game_running, speech_result, game_over, start_time

    clock = pygame.time.Clock()
    word_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 单词初始位置

    while True:
        screen.fill((250, 228, 217)) # 背景

        start_button = pygame.Rect(50, 500, 200, 50)
        end_button = pygame.Rect(550, 500, 200, 50)
        return_button = pygame.Rect(300, 500, 200, 50) # 按钮区域

        # 根据游戏状态显示按钮
        if not game_running and not game_over:
            pygame.draw.rect(screen, (162, 205, 97), start_button, border_radius=15)
            start_text = small_font.render("START", True, (250, 228, 217))
            screen.blit(start_text, (90, 510))
            draw_rules(screen)
        elif game_over:
            screen.fill((250, 228, 217))  # 背景
            end_text = small_font.render("GAME OVER", True, (210, 89, 98))
            end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(end_text, end_rect)
            score_text = small_font.render(f"FINAL SCORE: {score}", True, (20, 17, 31))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(score_text, score_rect)

            pygame.draw.rect(screen, (128, 175, 237), return_button, border_radius=15)
            return_text = small_font.render("RETURN", True, (250, 228, 217))
            return_rect = return_text.get_rect(center=return_button.center)
            screen.blit(return_text, return_rect)
        else:
            pygame.draw.rect(screen, (210, 89, 98), end_button, border_radius=15)
            end_text = small_font.render("END", True, (250, 228, 217))
            screen.blit(end_text, (600, 510))

            # 显示当前单词和颜色
            draw_text(current_word, current_color, screen, word_position)
            draw_score(score, screen)
            remaining_time = max(0, int(time_limit - (time.time() - start_time)))
            draw_time_remaining(remaining_time, screen)

            if remaining_time <= 0:
                end_game()

            # 处理语音识别结果
            if speech_result:
                if any(color in speech_result for color in COLORS):
                    score += 1
                    print("Correct! Current Score.", score)

                # 生成新单词和颜色
                current_word, current_color = get_random_color_and_word()
                speech_result = None
                word_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 重置单词位置

            # 更新单词位置
            word_position = (word_position[0], word_position[1] + word_scroll_speed)

            if word_position[1] > SCREEN_HEIGHT:
                current_word, current_color = get_random_color_and_word()
                word_position = (SCREEN_WIDTH // 2, 0)  # 重置单词位置到顶部

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # 按钮点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and not game_running and not game_over:
                    button_animation(start_button, (162, 205, 97), start_text, 1.2)
                    start_game()
                if end_button.collidepoint(event.pos) and game_running:
                    button_animation(end_button, (210, 89, 98), end_text, 1.2)
                    end_game()
                if return_button.collidepoint(event.pos) and game_over:
                    button_animation(return_button, (128, 175, 237), return_text, 1.2)
                    game_over = False

        clock.tick(60)

game_loop()
