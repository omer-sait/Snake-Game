import pygame
import random
import sys
from pygame.math import Vector2
import math

# Initialize pygame
pygame.init()

# Game constants
CELL_SIZE = 20
CELL_NUMBER = 30
PANEL_HEIGHT = 80
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER + PANEL_HEIGHT
FPS = 60

# Colors
GREEN = (175, 215, 70)
DARK_GREEN = (56, 74, 12)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)


# Game levels
LEVEL_EASY = 0
LEVEL_MEDIUM = 1
LEVEL_HARD = 2

class Snake:
    def __init__(self, color=BLACK):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.color = color
        self.original_color = color  # Güçlendirme bittikten sonra geri dönmek için orijinal rengi sakla
        
        # Basit grafikleri oluştur
        self.create_snake_graphics()
        
    def create_snake_graphics(self):
        # Farklı yönlere bakan 4 farklı baş oluşturalım
        self.head_right = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.head_left = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.head_up = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.head_down = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        
        # Sağa bakan baş
        pygame.draw.circle(self.head_right, self.color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
        # Göz beyazları - sağa bakıyor
        eye_size = CELL_SIZE // 6
        eye_pos_x = 3 * CELL_SIZE // 4
        eye_pos_y_top = CELL_SIZE // 3
        eye_pos_y_bottom = 2 * CELL_SIZE // 3
        pygame.draw.circle(self.head_right, WHITE, (eye_pos_x, eye_pos_y_top), eye_size)
        pygame.draw.circle(self.head_right, WHITE, (eye_pos_x, eye_pos_y_bottom), eye_size)
        # Göz bebekleri
        pupil_size = eye_size // 2
        pupil_offset = 1
        pygame.draw.circle(self.head_right, BLACK, (eye_pos_x + pupil_offset, eye_pos_y_top), pupil_size)
        pygame.draw.circle(self.head_right, BLACK, (eye_pos_x + pupil_offset, eye_pos_y_bottom), pupil_size)
        
        # Sola bakan baş
        pygame.draw.circle(self.head_left, self.color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
        # Göz beyazları - sola bakıyor
        eye_pos_x = CELL_SIZE // 4
        pygame.draw.circle(self.head_left, WHITE, (eye_pos_x, eye_pos_y_top), eye_size)
        pygame.draw.circle(self.head_left, WHITE, (eye_pos_x, eye_pos_y_bottom), eye_size)
        # Göz bebekleri
        pygame.draw.circle(self.head_left, BLACK, (eye_pos_x - pupil_offset, eye_pos_y_top), pupil_size)
        pygame.draw.circle(self.head_left, BLACK, (eye_pos_x - pupil_offset, eye_pos_y_bottom), pupil_size)
        
        # Yukarı bakan baş
        pygame.draw.circle(self.head_up, self.color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
        # Göz beyazları - yukarı bakıyor
        eye_pos_y = CELL_SIZE // 4
        eye_pos_x_left = CELL_SIZE // 3
        eye_pos_x_right = 2 * CELL_SIZE // 3
        pygame.draw.circle(self.head_up, WHITE, (eye_pos_x_left, eye_pos_y), eye_size)
        pygame.draw.circle(self.head_up, WHITE, (eye_pos_x_right, eye_pos_y), eye_size)
        # Göz bebekleri
        pygame.draw.circle(self.head_up, BLACK, (eye_pos_x_left, eye_pos_y - pupil_offset), pupil_size)
        pygame.draw.circle(self.head_up, BLACK, (eye_pos_x_right, eye_pos_y - pupil_offset), pupil_size)
        
        # Aşağı bakan baş
        pygame.draw.circle(self.head_down, self.color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
        # Göz beyazları - aşağı bakıyor
        eye_pos_y = 3 * CELL_SIZE // 4
        pygame.draw.circle(self.head_down, WHITE, (eye_pos_x_left, eye_pos_y), eye_size)
        pygame.draw.circle(self.head_down, WHITE, (eye_pos_x_right, eye_pos_y), eye_size)
        # Göz bebekleri
        pygame.draw.circle(self.head_down, BLACK, (eye_pos_x_left, eye_pos_y + pupil_offset), pupil_size)
        pygame.draw.circle(self.head_down, BLACK, (eye_pos_x_right, eye_pos_y + pupil_offset), pupil_size)
        
        # Mevcut baş görseli olarak sağa bakan başı atayalım (varsayılan)
        self.head = self.head_right
        
        # Vücut parçası - normal daire
        self.body_part = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.body_part, self.color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2 - 1)

    def change_color(self, color):
        self.color = color
        self.create_snake_graphics()
        
    def restore_original_color(self):
        self.color = self.original_color
        self.create_snake_graphics()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self, screen):
        # Skor paneli için kaydırma
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE + PANEL_HEIGHT)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:  # Head
                # Yılanın başını çiz
                screen.blit(self.head, block_rect)
            else:  # Body parts
                # Vücut parçalarını çiz
                screen.blit(self.body_part, block_rect)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            
        # Hareket yönüne göre başın görünümünü güncelle
        if self.direction.x > 0:  # Sağa
            self.head = self.head_right
        elif self.direction.x < 0:  # Sola
            self.head = self.head_left
        elif self.direction.y < 0:  # Yukarı
            self.head = self.head_up
        elif self.direction.y > 0:  # Aşağı
            self.head = self.head_down

    def add_block(self):
        self.new_block = True


class ScorePanel:
    @staticmethod
    def draw(screen, score, level, fruits_eaten, power_up_active=False, power_type="", power_duration=0, power_timer=0, high_score=0):
        # Üst panel
        panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)

        # Skor - Kalın yazı tipi
        font = pygame.font.SysFont('Arial', 22, bold=True)
        small_font = pygame.font.SysFont('Arial', 16, bold=True)
        
        # Skor metni
        score_text = font.render(f'SKOR: {score}', True, WHITE)
        screen.blit(score_text, (20, 15))
        
        # Yüksek skor (sağ üst köşe)
        if high_score > 0:
            high_score_text = small_font.render(f'EN YÜKSEK SKOR: {high_score}', True, YELLOW)
            high_score_rect = high_score_text.get_rect()
            screen.blit(high_score_text, (SCREEN_WIDTH - high_score_rect.width - 20, 45))

        # Seviye metni - seviye adı dinamik olarak oluşturulacak
        seviye_no = level + 1  # Seviyeler 0'dan başladığı için +1 ekliyoruz
        level_text = font.render(f'SEVİYE: {seviye_no}', True, WHITE)
        level_rect = level_text.get_rect()
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_rect.width // 2, 15))

        # Yem metni
        fruit_text = font.render(f'YEM: {fruits_eaten}/10', True, WHITE)
        fruit_rect = fruit_text.get_rect()
        screen.blit(fruit_text, (SCREEN_WIDTH - fruit_rect.width - 20, 15))
        
        # Alt satır: Güç-up bilgisi (aktifse)
        if power_up_active and power_duration > 0:
            # Kalan süreyi hesapla
            remaining_time = max(0, (power_duration - (pygame.time.get_ticks() - power_timer)) // 1000)
            
            # Güç tipine göre renk ve isim belirle
            if power_type == "speed":
                power_color = DARK_GREEN  # Daha koyu yeşil
                power_name = "HIZLANDIRMA"
            elif power_type == "invincibility":
                power_color = ORANGE
                power_name = "KALKAN"
            elif power_type == "eat_obstacles":
                power_color = PURPLE
                power_name = "ENGEL YEME"
            elif power_type == "slow":
                power_color = BLUE
                power_name = "YAVAŞLATMA"
            else:
                power_color = PINK
                power_name = "GÜÇ"
            
            # Güç bilgisini göster
            power_text = small_font.render(f"AKTİF GÜÇ: {power_name} - {remaining_time}s", True, power_color)
            power_rect = power_text.get_rect()
            screen.blit(power_text, (SCREEN_WIDTH // 2 - power_rect.width // 2, 50))
            
            # İlerleme çubuğu arka planı
            progress_bg_rect = pygame.Rect(SCREEN_WIDTH // 4, 45, SCREEN_WIDTH // 2, 10)
            pygame.draw.rect(screen, (70, 70, 70), progress_bg_rect)
            
            # İlerleme çubuğu - kalan süre
            if power_duration > 0:
                progress_width = int((power_duration - (pygame.time.get_ticks() - power_timer)) / power_duration * (SCREEN_WIDTH // 2))
                progress_rect = pygame.Rect(SCREEN_WIDTH // 4, 45, max(0, progress_width), 10)
                pygame.draw.rect(screen, power_color, progress_rect)

        # Panel alt çizgisi
        pygame.draw.line(screen, WHITE, (0, PANEL_HEIGHT-1), (SCREEN_WIDTH, PANEL_HEIGHT-1), 2)

class Fruit:
    def __init__(self):
        self.randomize()
        self.create_apple_surface()
        
    def create_apple_surface(self):
        # Elma için yüzey oluştur
        self.apple = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        
        # Elmanın ana kısmı (kırmızı daire)
        apple_radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(self.apple, RED, (CELL_SIZE // 2, CELL_SIZE // 2), apple_radius)
        
        # Elmanın sap kısmı
        stem_color = (139, 69, 19)  # Kahverengi
        stem_width = CELL_SIZE // 8
        stem_height = CELL_SIZE // 4
        pygame.draw.rect(self.apple, stem_color, 
                       (CELL_SIZE // 2 - stem_width // 2, 
                        CELL_SIZE // 2 - apple_radius - stem_height // 2,
                        stem_width, stem_height))
        
        # Elmanın yaprak kısmı
        leaf_color = (34, 139, 34)  # Yeşil
        leaf_points = [
            (CELL_SIZE // 2 + stem_width // 2, CELL_SIZE // 2 - apple_radius),  # Yaprağın başlangıç noktası
            (CELL_SIZE // 2 + stem_width // 2 + CELL_SIZE // 5, CELL_SIZE // 2 - apple_radius - CELL_SIZE // 6),  # Yaprağın uç noktası
            (CELL_SIZE // 2 + stem_width // 2 + CELL_SIZE // 10, CELL_SIZE // 2 - apple_radius - CELL_SIZE // 12),  # Yaprağın iç noktası
        ]
        pygame.draw.polygon(self.apple, leaf_color, leaf_points)
        
        # Elmanın parlak kısmı (yansıma efekti)
        highlight_radius = apple_radius // 3
        pygame.draw.circle(self.apple, (255, 200, 200), 
                         (CELL_SIZE // 2 - highlight_radius, CELL_SIZE // 2 - highlight_radius), 
                         highlight_radius)

    def draw(self, screen):
        # Skor paneli için kaydırma
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
        # Ekranın dışına çıkmamasını sağla
        if self.y < 0 or self.y >= CELL_NUMBER:
            self.y = CELL_NUMBER // 2

class Obstacle:
    def __init__(self, level):
        self.positions = []
        self.create_obstacles(level)
        self.obstacle_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.obstacle_surface.fill(DARK_GREEN)

    def create_obstacles(self, level):
        # self.positions listesi daha önce oluşturulmuş engelleri tutar
        # Level 0'da temiz başla, diğer seviyelerde eski engelleri koru
        if level == 0:
            self.positions = []
            
        # Her seviye için yeni engeller oluştur
        safe_zone = 5  # Yılanın başlangıç pozisyonu etrafında güvenli bölge
        
        # Seviye 0 (ilk seviye) engelleri
        if level == 0:
            # Temel engel sayısı - ilk seviye için daha az engel
            base_obstacles = 3
            
            # Rastgele engeller
            for _ in range(base_obstacles):
                # Rastgele pozisyonlar seç
                while True:
                    x = random.randint(0, CELL_NUMBER - 1)
                    y = random.randint(0, CELL_NUMBER - 1)
                    pos = Vector2(x, y)
                    
                    # Güvenli bölge kontrolü - yılanın başlangıç bölgesine engel koyma
                    if x < safe_zone and y < safe_zone:
                        continue
                        
                    # Pozisyon daha önce eklenmemişse ekle
                    if pos not in self.positions:
                        self.positions.append(pos)
                        break
        
        # Seviye 1 engelleri
        if level == 1:
            # Kenar duvarları eklemeye başla
            wall_length = 6  # Orta uzunlukta duvar
            
            # Rastgele bir kenarda duvar oluştur
            wall_position = random.choice(['top', 'right', 'bottom', 'left'])
            wall_start = random.randint(5, CELL_NUMBER - wall_length - 5)
            
            if wall_position == 'top':
                for i in range(wall_length):
                    pos = Vector2(wall_start + i, 5)
                    if pos not in self.positions:
                        self.positions.append(pos)
            elif wall_position == 'right':
                for i in range(wall_length):
                    pos = Vector2(CELL_NUMBER - 6, wall_start + i)
                    if pos not in self.positions:
                        self.positions.append(pos)
            elif wall_position == 'bottom':
                for i in range(wall_length):
                    pos = Vector2(wall_start + i, CELL_NUMBER - 6)
                    if pos not in self.positions:
                        self.positions.append(pos)
            elif wall_position == 'left':
                for i in range(wall_length):
                    pos = Vector2(5, wall_start + i)
                    if pos not in self.positions:
                        self.positions.append(pos)
                        
        # Seviye 2 engelleri
        if level == 2:
            # L şeklinde engeller ekle
            l_start_x = random.randint(10, CELL_NUMBER - 10)
            l_start_y = random.randint(10, CELL_NUMBER - 10)
            l_length = 5  # Orta büyüklükte L
            
            # L'nin dikey kısmı
            for i in range(l_length):
                pos = Vector2(l_start_x, l_start_y + i)
                if pos not in self.positions and 0 <= pos.x < CELL_NUMBER and 0 <= pos.y < CELL_NUMBER:
                    self.positions.append(pos)
            
            # L'nin yatay kısmı
            for i in range(1, l_length):
                pos = Vector2(l_start_x + i, l_start_y)
                if pos not in self.positions and 0 <= pos.x < CELL_NUMBER and 0 <= pos.y < CELL_NUMBER:
                    self.positions.append(pos)

    def draw(self, screen):
        # Skor paneli için kaydırma
        for pos in self.positions:
            obstacle_rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
            screen.blit(self.obstacle_surface, obstacle_rect)

    def is_collision(self, pos):
        for obstacle_pos in self.positions:
            if obstacle_pos == pos:
                return True
        return False

class PowerUp:
    def __init__(self, type="speed"):
        self.type = type  # speed, invincibility, slow, eat_obstacles
        self.active = False
        self.timer = 0
        self.duration = 8000  # 8 seconds in milliseconds
        self.pos = Vector2(-1, -1)  # Off-screen initially
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        
        # Tüm güçlendirmeler için temel elma şekli oluştur
        apple_radius = CELL_SIZE // 2 - 2
        
        # Güç tipine göre elma rengi belirle
        if self.type == "speed":
            apple_color = DARK_GREEN  # Hızlandırma için koyu yeşil elma
        elif self.type == "slow":
            apple_color = BLUE   # Yavaşlatma için mavi elma
        elif self.type == "invincibility":
            apple_color = ORANGE # Dokunulmazlık için turuncu elma
        elif self.type == "eat_obstacles":
            apple_color = PURPLE # Engel yeme için mor elma
        else:
            apple_color = PINK   # Varsayılan renk
            
        # Elmanın ana kısmı (renk güç tipine göre değişir)
        pygame.draw.circle(self.surface, apple_color, (CELL_SIZE // 2, CELL_SIZE // 2), apple_radius)
        
        # Elmanın sap kısmı
        stem_color = (139, 69, 19)  # Kahverengi
        stem_width = CELL_SIZE // 8
        stem_height = CELL_SIZE // 4
        pygame.draw.rect(self.surface, stem_color, 
                       (CELL_SIZE // 2 - stem_width // 2, 
                        CELL_SIZE // 2 - apple_radius - stem_height // 2,
                        stem_width, stem_height))
        
        # Elmanın yaprak kısmı
        leaf_color = (34, 139, 34)  # Yeşil
        leaf_points = [
            (CELL_SIZE // 2 + stem_width // 2, CELL_SIZE // 2 - apple_radius),  # Yaprağın başlangıç noktası
            (CELL_SIZE // 2 + stem_width // 2 + CELL_SIZE // 5, CELL_SIZE // 2 - apple_radius - CELL_SIZE // 6),  # Yaprağın uç noktası
            (CELL_SIZE // 2 + stem_width // 2 + CELL_SIZE // 10, CELL_SIZE // 2 - apple_radius - CELL_SIZE // 12),  # Yaprağın iç noktası
        ]
        pygame.draw.polygon(self.surface, leaf_color, leaf_points)
        
        # Elmanın parlaklık efekti (yansıma)
        highlight_radius = apple_radius // 3
        highlight_color = (255, 255, 255, 120)  # Yarı saydam beyaz
        pygame.draw.circle(self.surface, highlight_color, 
                         (CELL_SIZE // 2 - highlight_radius, CELL_SIZE // 2 - highlight_radius), 
                         highlight_radius)

    def spawn(self):
        if not self.active:
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
            self.active = True
            self.timer = 0

    def collect(self):
        self.active = False
        self.pos = Vector2(-1, -1)  # Move off-screen
        return self.type

    def update(self, dt):
        if self.active:
            self.timer += dt
            if self.timer >= self.duration:
                self.active = False
                self.pos = Vector2(-1, -1)  # Move off-screen

    def draw(self, screen):
        if self.active:
            power_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
            screen.blit(self.surface, power_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Yılan Oyunu')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = False
        
        # Kontrol tipi, varsayılan olarak ok tuşları
        self.control_type = "arrow_keys"
        
        # Ayarlar menüsü aktif mi
        self.settings_active = False
        self.settings_selection = 0
        self.paused = False
        self.level = LEVEL_EASY
        self.score = 0
        self.high_score = self.load_high_score()  # Yüksek skoru yükle
        self.fruits_eaten = 0
        self.level_up_threshold = 10  # Seviye atlamak için gereken meyve sayısı
        self.snake_speed = 10  # Başlangıç hızı
        self.snake_speeds = [10, 10, 10, 12, 14, 16, 18, 20, 22, 25]  # Seviye başına hızlar - Daha fazla seviye için
        
        # Menü değişkenleri
        self.in_menu = True
        self.menu_selection = 0  # 0: Başla, 1: Renk Seç, 2: Ayarlar, 3: Çıkış
        self.menu_options = ["BAŞLA", "RENK SEÇ", "AYARLAR", "ÇIKIŞ"]
        
        # Kontrol ayarları
        self.control_type = "arrow_keys"  # "arrow_keys" veya "wasd"
        self.settings_selection = 0  # 0: Ok tuşları, 1: WASD
        self.settings_active = False
        
        # Yılan rengi seçimi
        self.available_colors = [
            ("SİYAH", BLACK),
            ("MAVİ", BLUE),
            ("KIRMIZI", RED),
            ("MOR", PURPLE),
            ("TURUNCU", ORANGE),
            ("PEMBE", PINK)
        ]
        self.selected_color_index = 0
        self.color_selection_active = False

        # Ana oyun nesneleri
        self.snake = Snake(self.available_colors[self.selected_color_index][1])
        self.fruit = Fruit()
        self.obstacles = Obstacle(self.level)
        self.power_up = PowerUp(random.choice(["speed", "invincibility", "slow", "eat_obstacles"]))
        self.power_up_active = False
        self.power_up_effect_timer = 0
        self.power_up_effect_duration = 10000  # 10 saniye
        
        # Seviye atlama mesajı
        self.show_level_up_message = False
        self.level_up_message_timer = 0
        self.level_up_message_duration = 2000  # 2 saniye
        
        # Son basılan yön tuşu ve bir sonraki hareket için yön
        self.last_direction_key = None
        self.next_direction = Vector2(1, 0)
        self.direction_changed = False

        # Game over metni için font
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)

        # Hareket güncelleme olayı
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, int(1000 / self.snake_speed))

        # Power-up variables
        self.power_up_spawn_counter = 0  # Her 4 meyve yendiğinde güçlendirme çıkması için sayaç
        self.POWER_UP_SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.POWER_UP_SPAWN, 8000)  # Bu timer sadece standart 8 saniye için
        
        # Menü arkaplan yılanları
        self.menu_snakes = []
        self.create_menu_background_snakes()
        
        # Menü animasyonu için zamanlayıcı
        self.MENU_ANIMATION = pygame.USEREVENT + 2
        pygame.time.set_timer(self.MENU_ANIMATION, 150)  # 150ms'de bir hareket et
        
    def create_menu_background_snakes(self):
        # Menüdeki arkaplan yılanları
        snake_colors = [BLUE, RED, PURPLE, ORANGE, GREEN, YELLOW, PINK]
        for _ in range(5):  # 5 adet yılan oluştur
            # Rastgele konum ve yön
            start_x = random.randint(2, CELL_NUMBER - 3)
            start_y = random.randint(2, CELL_NUMBER - 3)
            
            # Rastgele yön
            directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
            direction = random.choice(directions)
            
            # Rastgele uzunluk (3-7 arası)
            length = random.randint(3, 7)
            
            # Rastgele renk
            color = random.choice(snake_colors)
            
            # Vücut parçalarını oluştur
            body = []
            for i in range(length):
                if direction.x != 0:  # Yatay hareket
                    body.append(Vector2(start_x - i * direction.x, start_y))
                else:  # Dikey hareket
                    body.append(Vector2(start_x, start_y - i * direction.y))
            
            # Yılanı listeye ekle (vücut, yön, renk, hareket sayacı)
            self.menu_snakes.append({
                "body": body,
                "direction": direction,
                "color": color,
                "move_counter": 0,
                "move_delay": random.randint(1, 3)  # Farklı hızlar için
            })
            
    def update_menu_snakes(self):
        for snake in self.menu_snakes:
            # Hareket sayacını artır ve hız kontrolü yap
            snake["move_counter"] += 1
            if snake["move_counter"] < snake["move_delay"]:
                continue
                
            snake["move_counter"] = 0
            
            # Yılanın başının mevcut konumunu al
            head_pos = snake["body"][0]
            
            # Rastgele yön değişimi (düşük olasılıkla)
            if random.random() < 0.1:  # %10 olasılıkla
                # Mevcut yöne dik yönlerden birini seç
                if snake["direction"].x != 0:  # Şu an yatay hareket ediyorsa
                    snake["direction"] = Vector2(0, random.choice([-1, 1]))
                else:  # Şu an dikey hareket ediyorsa
                    snake["direction"] = Vector2(random.choice([-1, 1]), 0)
            
            # Yeni baş konumu
            new_head = head_pos + snake["direction"]
            
            # Sınırları kontrol et ve gerekirse yönü değiştir
            if (new_head.x < 0 or new_head.x >= CELL_NUMBER or 
                new_head.y < 0 or new_head.y >= CELL_NUMBER):
                # Duvara çarptığında yönü tersine çevir
                snake["direction"] = Vector2(-snake["direction"].x, -snake["direction"].y)
                new_head = head_pos + snake["direction"]
            
            # Yılanın vücudunu güncelle
            snake["body"].insert(0, new_head)
            snake["body"].pop()
            
    def draw_menu_background_snakes(self):
        # Menüdeki yılanları çiz
        for snake in self.menu_snakes:
            for i, segment in enumerate(snake["body"]):
                x_pos = int(segment.x * CELL_SIZE)
                y_pos = int(segment.y * CELL_SIZE + PANEL_HEIGHT)
                
                # Yılan parçasını çiz
                if i == 0:  # Baş
                    # Daha büyük bir daire olarak baş
                    pygame.draw.circle(self.screen, snake["color"], 
                                     (x_pos + CELL_SIZE//2, y_pos + CELL_SIZE//2), 
                                     CELL_SIZE//2)
                    # Gözler
                    eye_radius = CELL_SIZE // 8
                    # Yöne göre göz pozisyonları
                    if snake["direction"].x > 0:  # Sağa bakıyor
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + 3*CELL_SIZE//4, y_pos + CELL_SIZE//3), 
                                         eye_radius)
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + 3*CELL_SIZE//4, y_pos + 2*CELL_SIZE//3), 
                                         eye_radius)
                    elif snake["direction"].x < 0:  # Sola bakıyor
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + CELL_SIZE//4, y_pos + CELL_SIZE//3), 
                                         eye_radius)
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + CELL_SIZE//4, y_pos + 2*CELL_SIZE//3), 
                                         eye_radius)
                    elif snake["direction"].y > 0:  # Aşağı bakıyor
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + CELL_SIZE//3, y_pos + 3*CELL_SIZE//4), 
                                         eye_radius)
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + 2*CELL_SIZE//3, y_pos + 3*CELL_SIZE//4), 
                                         eye_radius)
                    else:  # Yukarı bakıyor
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + CELL_SIZE//3, y_pos + CELL_SIZE//4), 
                                         eye_radius)
                        pygame.draw.circle(self.screen, WHITE, 
                                         (x_pos + 2*CELL_SIZE//3, y_pos + CELL_SIZE//4), 
                                         eye_radius)
                else:  # Vücut
                    pygame.draw.circle(self.screen, snake["color"], 
                                     (x_pos + CELL_SIZE//2, y_pos + CELL_SIZE//2), 
                                     CELL_SIZE//2 - 1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Fare tıklaması kontrolü
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tıklama
                    if not self.game_active:
                        if self.in_menu:
                            self.handle_menu_mouse_click(event.pos)
                        elif self.color_selection_active:
                            self.handle_color_selection_mouse_click(event.pos)
                        elif self.settings_active:
                            self.handle_settings_mouse_click(event.pos)
            
            # Fare hareketi kontrolü (menü için hover efekti)
            if event.type == pygame.MOUSEMOTION:
                if not self.game_active:
                    if self.in_menu:
                        self.handle_menu_mouse_hover(event.pos)
                    elif self.color_selection_active:
                        self.handle_color_selection_mouse_hover(event.pos)
                    elif self.settings_active:
                        # Ayarlar menüsünde fare etkileşimi doğrudan ayarlar çizim fonksiyonunda işleniyor
                        pass
            
            if event.type == pygame.KEYDOWN:
                # Menü navigasyonu
                if not self.game_active:
                    if self.in_menu:
                        self.handle_main_menu_input(event.key)
                    elif self.color_selection_active:
                        self.handle_color_selection_input(event.key)
                    elif self.settings_active:
                        # Ayarlar menüsü tuş kontrolleri
                        if event.key == pygame.K_ESCAPE:
                            self.settings_active = False
                            self.in_menu = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            # Ok tuşları ve WASD arasında geçiş
                            if self.settings_selection == 0:  # Ok tuşlarından -> WASD'ye
                                self.settings_selection = 1
                                self.control_type = "wasd"
                            else:  # WASD'den -> Ok tuşlarına
                                self.settings_selection = 0
                                self.control_type = "arrow_keys"
                        elif event.key == pygame.K_RETURN:
                            # Ayarları kaydet ve menüye dön
                            self.settings_active = False
                            self.in_menu = True
                    else:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.game_active = True
                # Oyun içi kontroller
                else:
                    # Space tuşu ile durdurma/devam etme
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    
                    # ESC tuşu hala menüye dönme olarak kullanılabilir
                    if event.key == pygame.K_ESCAPE:
                        self.game_active = False
                        self.in_menu = True
                    
                    if not self.paused:
                        # Yön tuşlarını kontrol et (Ok tuşları veya WASD), bir sonraki güncelleme için yeni yönü kaydet
                        if self.control_type == "arrow_keys":
                            # Ok tuşları kontrolü
                            if event.key == pygame.K_UP and self.snake.direction.y != 1:
                                self.next_direction = Vector2(0, -1)
                                self.direction_changed = True
                            if event.key == pygame.K_DOWN and self.snake.direction.y != -1:
                                self.next_direction = Vector2(0, 1)
                                self.direction_changed = True
                            if event.key == pygame.K_LEFT and self.snake.direction.x != 1:
                                self.next_direction = Vector2(-1, 0)
                                self.direction_changed = True
                            if event.key == pygame.K_RIGHT and self.snake.direction.x != -1:
                                self.next_direction = Vector2(1, 0)
                                self.direction_changed = True
                        else:  # control_type == "wasd"
                            # WASD kontrolü
                            if event.key == pygame.K_w and self.snake.direction.y != 1:
                                self.next_direction = Vector2(0, -1)
                                self.direction_changed = True
                            if event.key == pygame.K_s and self.snake.direction.y != -1:
                                self.next_direction = Vector2(0, 1)
                                self.direction_changed = True
                            if event.key == pygame.K_a and self.snake.direction.x != 1:
                                self.next_direction = Vector2(-1, 0)
                                self.direction_changed = True
                            if event.key == pygame.K_d and self.snake.direction.x != -1:
                                self.next_direction = Vector2(1, 0)
                                self.direction_changed = True
            
            if event.type == self.SCREEN_UPDATE and self.game_active and not self.paused:
                # Hareket öncesi yön değişikliği yapıldıysa yeni yönü ayarla
                if self.direction_changed:
                    self.snake.direction = self.next_direction
                    self.direction_changed = False
                self.update()
            
            if event.type == self.POWER_UP_SPAWN and self.game_active and not self.paused:
                if random.random() < 0.3:  # %30 şansla
                    self.power_up.type = random.choice(["speed", "invincibility", "slow", "eat_obstacles"])
                    self.power_up.create_surface()
                    self.power_up.spawn()
                    
            # Menü animasyonu (yılanların hareketlendirilmesi)
            if event.type == self.MENU_ANIMATION and (self.in_menu or self.color_selection_active or self.settings_active):
                self.update_menu_snakes()
                    
    def handle_menu_mouse_click(self, pos):
        menu_y_start = SCREEN_HEIGHT//2 - 30
        menu_y_spacing = 70
        button_width, button_height = 240, 50
        
        for i, option in enumerate(self.menu_options):
            menu_rect = pygame.Rect(
                SCREEN_WIDTH//2 - button_width//2,
                menu_y_start + i * menu_y_spacing - button_height//2,
                button_width,
                button_height
            )
            
            if menu_rect.collidepoint(pos):
                if i == 0:  # BAŞLA
                    self.in_menu = False
                    self.game_active = True
                    self.reset_game()
                elif i == 1:  # RENK SEÇ
                    self.in_menu = False
                    self.color_selection_active = True
                elif i == 2:  # AYARLAR
                    self.in_menu = False
                    self.settings_active = True
                elif i == 3:  # ÇIKIŞ
                    self.running = False
                break
    
    def handle_menu_mouse_hover(self, pos):
        menu_y_start = SCREEN_HEIGHT//2 - 30
        menu_y_spacing = 70
        button_width, button_height = 240, 50
        
        for i, option in enumerate(self.menu_options):
            menu_rect = pygame.Rect(
                SCREEN_WIDTH//2 - button_width//2,
                menu_y_start + i * menu_y_spacing - button_height//2,
                button_width,
                button_height
            )
            
            if menu_rect.collidepoint(pos):
                self.menu_selection = i
                break
    
    def handle_color_selection_mouse_click(self, pos):
        # Renk butonları değişkenleri (draw_color_selection_menu ile aynı olmalı)
        color_button_size = 60
        color_spacing = 80
        color_y = SCREEN_HEIGHT//2
        color_start_x = SCREEN_WIDTH//2 - (len(self.available_colors) * color_spacing)//2 + color_spacing//2
        
        # Renk butonları tıklama kontrolü
        for i, (color_name, color_value) in enumerate(self.available_colors):
            # Buton x pozisyonu
            color_x = color_start_x + i * color_spacing
            
            # Renk butonunun kendisi bir daire
            button_rect = pygame.Rect(
                color_x - color_button_size//2,
                color_y - color_button_size//2,
                color_button_size,
                color_button_size
            )
            
            # Tıklama kontrolü için kare kullan (daire tıklama tespiti için)
            if button_rect.collidepoint(pos):
                # Rengi seç ve ana menüye dön
                self.selected_color_index = i
                selected_color = self.available_colors[self.selected_color_index][1]
                self.snake.change_color(selected_color)
                self.color_selection_active = False
                self.in_menu = True
                break
                
        # Geri butonu tıklama kontrolü (ekranın alt kısmında)
        back_button_rect = pygame.Rect(
            SCREEN_WIDTH//2 - 150, 
            SCREEN_HEIGHT - 60 - 20, 
            300, 
            40
        )
        if back_button_rect.collidepoint(pos):
            self.color_selection_active = False
            self.in_menu = True
            
    def handle_color_selection_mouse_hover(self, pos):
        # Renk butonları değişkenleri (handle_color_selection_mouse_click ile aynı olmalı)
        color_button_size = 60
        color_spacing = 80
        color_y = SCREEN_HEIGHT//2
        color_start_x = SCREEN_WIDTH//2 - (len(self.available_colors) * color_spacing)//2 + color_spacing//2
        
        # Renk butonları hover kontrolü
        for i, (color_name, color_value) in enumerate(self.available_colors):
            # Buton x pozisyonu
            color_x = color_start_x + i * color_spacing
            
            # Daire şeklindeki butonun kare hitbox'u
            button_rect = pygame.Rect(
                color_x - color_button_size//2,
                color_y - color_button_size//2,
                color_button_size,
                color_button_size
            )
            
            if button_rect.collidepoint(pos):
                self.selected_color_index = i
                break
                    
    def handle_main_menu_input(self, key):
        # Seçilen kontrol tipine göre tuş kontrolü
        if self.control_type == "arrow_keys":
            up_key = pygame.K_UP
            down_key = pygame.K_DOWN
        else:  # WASD kontrolleri
            up_key = pygame.K_w
            down_key = pygame.K_s
        
        if key == up_key:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
        elif key == down_key:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
        elif key == pygame.K_RETURN:
            if self.menu_selection == 0:  # BAŞLA
                self.in_menu = False
                self.game_active = True
                self.reset_game()
            elif self.menu_selection == 1:  # RENK SEÇ
                self.in_menu = False
                self.color_selection_active = True
            elif self.menu_selection == 2:  # AYARLAR
                self.in_menu = False
                self.settings_active = True
            elif self.menu_selection == 3:  # ÇIKIŞ
                self.running = False
                
    def handle_settings_mouse_click(self, pos):
        # Ayarlar menüsündeki kontrol tipi butonları
        settings_y_start = SCREEN_HEIGHT//2 - 50
        button_width, button_height = 150, 40
        
        # Ok tuşları butonu
        arrow_button = pygame.Rect(
            SCREEN_WIDTH//2 - 180, 
            settings_y_start + 50, 
            button_width, 
            button_height
        )
        
        # WASD butonu
        wasd_button = pygame.Rect(
            SCREEN_WIDTH//2 + 30, 
            settings_y_start + 50, 
            button_width, 
            button_height
        )
        
        # Butonlara tıklama kontrolü
        if arrow_button.collidepoint(pos):
            self.control_type = "arrow_keys"
            self.settings_selection = 0
        
        if wasd_button.collidepoint(pos):
            self.control_type = "wasd"
            self.settings_selection = 1
        
        # Geri butonu tıklama kontrolü
        back_button_width, back_button_height = 200, 40
        back_button = pygame.Rect(
            SCREEN_WIDTH//2 - back_button_width//2,
            SCREEN_HEIGHT - 100,
            back_button_width,
            back_button_height
        )
        
        if back_button.collidepoint(pos):
            self.settings_active = False
            self.in_menu = True
            
    def handle_color_selection_input(self, key):
        # Seçilen kontrol tipine göre tuş kontrolü
        if self.control_type == "arrow_keys":
            up_key = pygame.K_UP
            down_key = pygame.K_DOWN
        else:  # WASD kontrolleri
            up_key = pygame.K_w
            down_key = pygame.K_s
            
        if key == up_key:
            self.selected_color_index = (self.selected_color_index - 1) % len(self.available_colors)
        elif key == down_key:
            self.selected_color_index = (self.selected_color_index + 1) % len(self.available_colors)
        elif key == pygame.K_RETURN:
            # Rengi kaydet ve ana menüye dön
            selected_color = self.available_colors[self.selected_color_index][1]
            self.snake.change_color(selected_color)
            self.color_selection_active = False
            self.in_menu = True
        elif key == pygame.K_ESCAPE:
            # Değişiklik yapmadan ana menüye dön
            self.color_selection_active = False
            self.in_menu = True
        
    def update(self):
        # Yılanı hareket ettir
        self.snake.move()
        
        # Yılanın kendine çarpması kontrolü
        self.check_self_collision()
        
        # Yılanın duvara çarpması kontrolü
        self.check_wall_collision()
        
        # Yılanın engele çarpması kontrolü
        self.check_obstacle_collision()
        
        # Yılanın meyveyi yemesi kontrolü
        self.check_fruit_collection()
        
        # Yılanın güç-up'ı alması kontrolü
        self.check_power_up_collection()
        
        # Güç-up süresini güncelle
        current_time = pygame.time.get_ticks()
        if self.power_up_active and current_time - self.power_up_effect_timer > self.power_up_effect_duration:
            self.power_up_active = False
            # Hızı normal seviyeye geri getir
            pygame.time.set_timer(self.SCREEN_UPDATE, int(1000 / self.snake_speeds[self.level]))
            # Yılanın rengini geri getir
            self.snake.restore_original_color()

    def check_self_collision(self):
        # Yılanın başı, vücudunun herhangi bir parçasına çarparsa oyun biter
        if self.snake.body[0] in self.snake.body[1:]:
            if not self.power_up_active or self.power_up.type != "invincibility":
                self.game_active = False
                self.in_menu = True  # Menüye dön

    def check_wall_collision(self):
        # Eğer yılan duvardan geçiyorsa (invincibility modu varsa), diğer taraftan çıkmasını sağla
        head = self.snake.body[0]
        
        if self.power_up_active and self.power_up.type == "invincibility":
            # Ekranın diğer tarafından çıksın
            if head.x < 0:
                # Sol kenardan çıktı, sağ kenardan giriş yap
                self.snake.body[0] = Vector2(CELL_NUMBER - 1, head.y)
            elif head.x >= CELL_NUMBER:
                # Sağ kenardan çıktı, sol kenardan giriş yap
                self.snake.body[0] = Vector2(0, head.y)
            elif head.y < 0:
                # Üst kenardan çıktı, alt kenardan giriş yap
                self.snake.body[0] = Vector2(head.x, CELL_NUMBER - 1)
            elif head.y >= CELL_NUMBER:
                # Alt kenardan çıktı, üst kenardan giriş yap
                self.snake.body[0] = Vector2(head.x, 0)
        # Duvara çarparsa ve invincibility yoksa, oyun biter
        elif (head.x < 0 or head.x >= CELL_NUMBER or head.y < 0 or head.y >= CELL_NUMBER):
            self.game_active = False
            self.in_menu = True  # Menüye dön

    def check_obstacle_collision(self):
        # Yılanın başı engele çarparsa oyun biter veya engeli ye (eat_obstacles power-up)
        if self.obstacles.is_collision(self.snake.body[0]):
            if self.power_up_active and self.power_up.type == "eat_obstacles":
                # Engeli ye - engeli listeden çıkar
                for i, pos in enumerate(self.obstacles.positions):
                    if pos == self.snake.body[0]:
                        del self.obstacles.positions[i]
                        # Yılanın boyunu artır ve skoru artır
                        self.snake.add_block()
                        self.score += 20
                        break
                
                # Ekran sınırlarını kontrol et (yılanın ekranın dışına çıkmamasını sağla)
                head = self.snake.body[0]
                if head.x < 0:
                    self.snake.body[0] = Vector2(0, head.y)
                elif head.x >= CELL_NUMBER:
                    self.snake.body[0] = Vector2(CELL_NUMBER - 1, head.y)
                elif head.y < 0:
                    self.snake.body[0] = Vector2(head.x, 0)
                elif head.y >= CELL_NUMBER:
                    self.snake.body[0] = Vector2(head.x, CELL_NUMBER - 1)
                    
            elif not self.power_up_active or self.power_up.type != "invincibility":
                self.game_active = False
                self.in_menu = True  # Menüye dön

    def check_fruit_collection(self):
        # Yılanın başı meyve ile aynı konumdaysa, meyveyi yemiş demektir
        if self.snake.body[0] == self.fruit.pos:
            # Meyveyi yeni bir konuma taşı
            self.place_fruit()
            # Yılanın boyunu artır
            self.snake.add_block()
            # Skoru ve yenilen meyve sayısını artır
            self.score += 10
            self.fruits_eaten += 1
            
            # Her 4 meyvede bir güçlendirme ortaya çıkar
            self.power_up_spawn_counter += 1
            if self.power_up_spawn_counter >= 4:
                self.power_up.type = random.choice(["speed", "invincibility", "slow", "eat_obstacles"])
                self.power_up.create_surface()
                self.power_up.spawn()
                self.power_up_spawn_counter = 0
            
            # Seviye atlama kontrolü
            if self.fruits_eaten >= self.level_up_threshold:
                self.level_up()

    def check_power_up_collection(self):
        # Yılanın başı power-up ile aynı konumdaysa, power-up'ı almış demektir
        if self.power_up.active and self.snake.body[0] == self.power_up.pos:
            power_type = self.power_up.collect()
            self.apply_power_up(power_type)

    def apply_power_up(self, power_type):
        # Bir önceki güç aktifse, önce rengimizi geri alalım
        if self.power_up_active:
            self.snake.restore_original_color()
            
        self.power_up_active = True
        self.power_up_effect_timer = pygame.time.get_ticks()
        
        if power_type == "speed":
            # Hızı artır
            pygame.time.set_timer(self.SCREEN_UPDATE, int(1000 / (self.snake_speeds[self.level] * 1.5)))
            self.snake.change_color(DARK_GREEN)  # Hızlandırma için yılanı koyu yeşil yap
        elif power_type == "slow":
            # Hızı azalt
            pygame.time.set_timer(self.SCREEN_UPDATE, int(1000 / (self.snake_speeds[self.level] * 0.7)))
            self.snake.change_color(BLUE)  # Yavaşlatma için yılanı mavi yap
        elif power_type == "eat_obstacles":
            # Engelleri yiyebilme güçlendirmesi
            self.snake.change_color(PURPLE)  # Engel yeme modu rengi
        elif power_type == "invincibility":
            # Geçici dokunulmazlık (hiçbir şey yapma, kontrollerde kullanılacak)
            self.snake.change_color(ORANGE)  # Dokunulmazlık rengi

    def place_fruit(self):
        while True:
            self.fruit.randomize()
            # Meyvenin yılanın üzerine veya engellerin üzerine düşmemesini sağla
            if (self.fruit.pos not in self.snake.body and 
                not self.obstacles.is_collision(self.fruit.pos) and
                (not self.power_up.active or self.fruit.pos != self.power_up.pos)):
                break

    def level_up(self):
        # Bu fonksiyon level atlama işlemlerini gerçekleştirir
        
        # Seviyeyi artır, maksimum seviyeyi kontrol etme - her zaman yeni seviye ekle
        self.level += 1
        
        # Seviye değişimini göster
        print(f"Seviye atlandı! Yeni seviye: {self.level + 1}")
        
        # Yeni seviye için engelleri ekle (eski engelleri koruyarak)
        self.obstacles.create_obstacles(self.level)
        
        # Yenilen meyve sayacını sıfırla
        self.fruits_eaten = 0
        
        # Yeni meyveyi yerleştir (yılanın veya engelin üstüne düşmemesi için)
        self.place_fruit()
        
        # Seviye atlandığını göstermek için ekranda bir mesaj göster
        self.show_level_up_message = True
        self.level_up_message_timer = pygame.time.get_ticks()
        self.level_up_message_duration = 2000  # 2 saniye
            
    def reset_game(self):
        self.level = LEVEL_EASY
        self.score = 0
        self.fruits_eaten = 0
        self.power_up_spawn_counter = 0  # Güçlendirme sayacını sıfırla
        self.snake_speed = self.snake_speeds[self.level]
        pygame.time.set_timer(self.SCREEN_UPDATE, int(1000 / self.snake_speed))
        
        # Yılanı sıfırla ama mevcut rengi koru
        current_color = self.snake.color
        self.snake.reset()
        if current_color != BLACK:  # Eğer daha önce renk seçildiyse o rengi kullan
            self.snake.change_color(current_color)
        
        self.obstacles = Obstacle(self.level)
        self.place_fruit()
        self.power_up_active = False
        self.power_up.active = False
        self.power_up.pos = Vector2(-1, -1)  # Off-screen
        
        # Hareket sistemi değişkenlerini sıfırla
        self.next_direction = Vector2(1, 0)
        self.direction_changed = False
        
        # Oyun aktif duruma getir
        self.game_active = True
        self.paused = False
        
        # Menü durumlarını sıfırla (oyun tekrar başladığında)
        self.in_menu = False
        self.color_selection_active = False
        self.settings_active = False

    def draw(self):
        self.screen.fill(GREEN)
        
        # Arka plan karelerini çiz
        self.draw_grid()
        
        # Oyun aktifse oyun elemanlarını çiz
        if self.game_active:
            self.fruit.draw(self.screen)
            self.snake.draw(self.screen)
            self.obstacles.draw(self.screen)
            if self.power_up.active:
                self.power_up.draw(self.screen)
            
            # Skor panelini çiz (güç-up bilgisiyle birlikte)
            ScorePanel.draw(
                self.screen, 
                self.score, 
                self.level, 
                self.fruits_eaten, 
                self.power_up_active, 
                self.power_up.type if self.power_up_active else "", 
                self.power_up_effect_duration, 
                self.power_up_effect_timer,
                self.high_score
            )
            
            # Seviye atlama mesajını göster (varsa)
            if hasattr(self, 'show_level_up_message') and self.show_level_up_message:
                current_time = pygame.time.get_ticks()
                if current_time - self.level_up_message_timer < self.level_up_message_duration:
                    self.draw_level_up_message()
                else:
                    self.show_level_up_message = False
            
            # Oyun duraklatılmışsa, duraklatma mesajını göster
            if self.paused:
                self.draw_pause_screen()
        else:
            # Oyun aktif değilse, oyunu başlatma veya oyun sonu ekranını göster
            if self.score == 0:
                self.draw_start_screen()
            else:
                self.draw_game_over_screen()
        
        pygame.display.update()
        
    def draw_grid(self):
        # Arka plan için kareler çiz
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                # Satranç tahtası deseni oluştur
                if (row + col) % 2 == 0:
                    # Daha açık yeşil renkli hücreler
                    color = (175, 215, 70)  # GREEN
                else:
                    # Daha koyu yeşil renkli hücreler
                    color = (167, 209, 61)  # Biraz daha koyu yeşil
                
                # Hücre dikdörtgenini çiz
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_start_screen(self):
        if self.in_menu:
            self.draw_main_menu()
        elif self.color_selection_active:
            self.draw_color_selection_menu()
        elif self.settings_active:
            self.draw_settings_menu()
        else:
            title_text = self.font.render("YILAN OYUNU", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            
            start_text = self.small_font.render("Başlamak için SPACE tuşuna basın", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
            
    def draw_main_menu(self):
        # Önce arka plandaki yılanları çiz (menünün arkasına)
        self.draw_menu_background_snakes()
        
        # Menü arka planı (yarı saydam)
        menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        menu_overlay.fill((0, 0, 0, 180))  # Daha saydam arka plan
        self.screen.blit(menu_overlay, (0, 0))
        
        # Oyun başlığı - Gölgeli ve daha büyük
        shadow_offset = 3
        title_shadow = self.title_font.render("YILAN OYUNU", True, (60, 60, 0))  # Daha koyu gölge rengi
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + shadow_offset, SCREEN_HEIGHT//2 - 150 + shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.title_font.render("YILAN OYUNU", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Menü seçenekleri - Daha şık butonlar
        menu_y_start = SCREEN_HEIGHT//2 - 30
        menu_y_spacing = 70
        button_width, button_height = 240, 50
        
        # Fare pozisyonunu al
        mouse_pos = pygame.mouse.get_pos()
        
        for i, option in enumerate(self.menu_options):
            # Buton koordinatları
            button_rect = pygame.Rect(
                SCREEN_WIDTH//2 - button_width//2, 
                menu_y_start + i * menu_y_spacing - button_height//2, 
                button_width, 
                button_height
            )
            
            # Seçili menü öğesi veya fare üzerindeyse vurgulanır
            is_selected = (i == self.menu_selection)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            # Buton rengi ve stil belirle
            if is_selected or is_hovered:
                # Aktif butonlar için daha parlak renk ve daha kalın kenar
                button_color = DARK_GREEN
                text_color = YELLOW
                border_width = 3
                text = option
            else:
                button_color = (30, 50, 10)  # Daha koyu buton
                text_color = WHITE
                border_width = 1
                text = option
            
            # Butonu çiz
            pygame.draw.rect(self.screen, button_color, button_rect, 0, 10)  # Kenarları yuvarlatılmış buton
            pygame.draw.rect(self.screen, text_color, button_rect, border_width, 10)  # Kenar
            
            # Buton metni
            menu_text = self.font.render(text, True, text_color)
            menu_rect = menu_text.get_rect(center=button_rect.center)
            self.screen.blit(menu_text, menu_rect)
            
            # Eğer seçili ise ok işaretlerini göster
            if is_selected:
                arrow_size = 10
                # Sol ok
                pygame.draw.polygon(self.screen, YELLOW, [
                    (button_rect.left - 15, button_rect.centery),
                    (button_rect.left - 15 - arrow_size, button_rect.centery - arrow_size),
                    (button_rect.left - 15 - arrow_size, button_rect.centery + arrow_size),
                ])
                # Sağ ok
                pygame.draw.polygon(self.screen, YELLOW, [
                    (button_rect.right + 15, button_rect.centery),
                    (button_rect.right + 15 + arrow_size, button_rect.centery - arrow_size),
                    (button_rect.right + 15 + arrow_size, button_rect.centery + arrow_size),
                ])
        
        # Yönergeler - Daha şık bir kutu içinde
        info_box = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 90, 400, 60)
        pygame.draw.rect(self.screen, (30, 30, 30, 200), info_box, 0, 10)
        pygame.draw.rect(self.screen, (100, 100, 100), info_box, 1, 10)
        
        # Kontrol tipine göre tuş bilgilerini göster
        if self.control_type == "arrow_keys":
            controls_text1 = self.small_font.render("Yukarı/Aşağı: Seçim", True, WHITE)
        else:  # WASD kontrolleri
            controls_text1 = self.small_font.render("W/S: Seçim", True, WHITE)
            
        controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT - 60))
        
        controls_text2 = self.small_font.render("Enter/Tık: Onayla", True, WHITE)
        controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH//2 + 80, SCREEN_HEIGHT - 60))
        
        self.screen.blit(controls_text1, controls_rect1)
        self.screen.blit(controls_text2, controls_rect2)
        
    def draw_settings_menu(self):
        # Önce arka plandaki yılanları çiz (menünün arkasına)
        self.draw_menu_background_snakes()
        
        # Menü arka planı
        menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        menu_overlay.fill((0, 0, 0, 180))  # Koyu saydam arka plan
        self.screen.blit(menu_overlay, (0, 0))
        
        # Menü başlığı - Gölgeli
        shadow_offset = 2
        title_shadow = self.title_font.render("AYARLAR", True, (100, 100, 0))
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + shadow_offset, SCREEN_HEIGHT//2 - 150 + shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.title_font.render("AYARLAR", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Fare pozisyonunu al
        mouse_pos = pygame.mouse.get_pos()
        
        # Ayarlar seçenekleri
        settings_y_start = SCREEN_HEIGHT//2 - 50
        
        # Kontrol tipi seçimi
        control_text = self.font.render("Kontrol Tipi:", True, WHITE)
        control_rect = control_text.get_rect(topleft=(SCREEN_WIDTH//2 - 200, settings_y_start))
        self.screen.blit(control_text, control_rect)
        
        # Kontrol tipi butonları
        button_width, button_height = 150, 40
        control_button_spacing = 20
        
        # Ok tuşları butonu
        arrow_button = pygame.Rect(
            SCREEN_WIDTH//2 - 180, 
            settings_y_start + 50, 
            button_width, 
            button_height
        )
        
        # WASD butonu
        wasd_button = pygame.Rect(
            SCREEN_WIDTH//2 + 30, 
            settings_y_start + 50, 
            button_width, 
            button_height
        )
        
        # Seçili kontrol tipine göre buton renklerini belirle
        arrow_color = DARK_GREEN if self.control_type == "arrow_keys" else (30, 50, 10)
        wasd_color = DARK_GREEN if self.control_type == "wasd" else (30, 50, 10)
        
        # Butonları çiz
        pygame.draw.rect(self.screen, arrow_color, arrow_button, 0, 10)
        pygame.draw.rect(self.screen, wasd_color, wasd_button, 0, 10)
        
        # Buton kenarları
        arrow_border_color = YELLOW if self.control_type == "arrow_keys" else WHITE
        wasd_border_color = YELLOW if self.control_type == "wasd" else WHITE
        
        pygame.draw.rect(self.screen, arrow_border_color, arrow_button, 2, 10)
        pygame.draw.rect(self.screen, wasd_border_color, wasd_button, 2, 10)
        
        # Buton metinleri
        arrow_text = self.font.render("Ok Tuşları", True, WHITE)
        arrow_text_rect = arrow_text.get_rect(center=arrow_button.center)
        self.screen.blit(arrow_text, arrow_text_rect)
        
        wasd_text = self.font.render("WASD", True, WHITE)
        wasd_text_rect = wasd_text.get_rect(center=wasd_button.center)
        self.screen.blit(wasd_text, wasd_text_rect)
        
        # Butonların fare üzerinde mi kontrolü
        if arrow_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, YELLOW, arrow_button, 3, 10)
            if pygame.mouse.get_pressed()[0]:
                self.control_type = "arrow_keys"
        
        if wasd_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, YELLOW, wasd_button, 3, 10)
            if pygame.mouse.get_pressed()[0]:
                self.control_type = "wasd"
        
        # Geri butonu
        back_button_width, back_button_height = 200, 40
        back_button = pygame.Rect(
            SCREEN_WIDTH//2 - back_button_width//2,
            SCREEN_HEIGHT - 100,
            back_button_width,
            back_button_height
        )
        
        # Geri butonu fare üzerinde mi kontrolü
        is_back_hovered = back_button.collidepoint(mouse_pos)
        back_button_color = DARK_GREEN if is_back_hovered else (30, 50, 10)
        back_border_color = YELLOW if is_back_hovered else WHITE
        back_border_width = 3 if is_back_hovered else 1
        
        # Geri butonunu çiz
        pygame.draw.rect(self.screen, back_button_color, back_button, 0, 10)
        pygame.draw.rect(self.screen, back_border_color, back_button, back_border_width, 10)
        
        # Geri butonu metni
        back_text = self.font.render("KAYDET", True, back_border_color)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Geri butonuna tıklama
        if back_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.settings_active = False
            self.in_menu = True
        
        # Yönergeler
        info_box = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 50, 500, 30)
        controls_text = self.small_font.render("Tıklayarak kontrol tipini değiştirin ve kaydedin", True, WHITE)
        controls_rect = controls_text.get_rect(center=info_box.center)
        self.screen.blit(controls_text, controls_rect)
        
    def draw_color_selection_menu(self):
        # Önce arka plandaki yılanları çiz (menünün arkasına)
        self.draw_menu_background_snakes()
        
        # Menü arka planı
        menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        menu_overlay.fill((0, 0, 0, 180))  # Koyu saydam arka plan
        self.screen.blit(menu_overlay, (0, 0))
        
        # Menü başlığı - Gölgeli
        shadow_offset = 2
        title_shadow = self.title_font.render("YILAN RENGİ SEÇİN", True, (100, 100, 0))
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + shadow_offset, SCREEN_HEIGHT//2 - 150 + shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.title_font.render("YILAN RENGİ SEÇİN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Fare pozisyonunu al
        mouse_pos = pygame.mouse.get_pos()
        
        # Renk seçenekleri - Modern yuvarlak kutular içinde
        color_button_size = 60
        color_spacing = 80
        color_y = SCREEN_HEIGHT//2
        
        # Renk butonları için merkez x pozisyonu
        color_start_x = SCREEN_WIDTH//2 - (len(self.available_colors) * color_spacing)//2 + color_spacing//2
        
        for i, (color_name, color_value) in enumerate(self.available_colors):
            # Buton x pozisyonu
            color_x = color_start_x + i * color_spacing
            
            # Renk adını çiz (butonun üzerinde)
            name_color = color_value if i == self.selected_color_index else WHITE
            name_text = self.small_font.render(color_name, True, name_color)
            name_rect = name_text.get_rect(center=(color_x, color_y - color_button_size//2 - 20))
            self.screen.blit(name_text, name_rect)
            
            # Renk butonları (daire şeklinde)
            # İç dolgu (solid renk)
            pygame.draw.circle(self.screen, color_value, (color_x, color_y), color_button_size//2)
            
            # Seçili rengin etrafına parlak bir çerçeve çiz
            if i == self.selected_color_index:
                pygame.draw.circle(self.screen, WHITE, (color_x, color_y), color_button_size//2 + 3, 3)  # Parlak beyaz çerçeve
                # Ok işareti (seçili butonu belirtmek için)
                arrow_width, arrow_height = 15, 10
                pygame.draw.polygon(self.screen, WHITE, [
                    (color_x, color_y + color_button_size//2 + 15),  # Aşağı ok tepe noktası
                    (color_x - arrow_width//2, color_y + color_button_size//2 + 15 - arrow_height),  # Sol alt köşe
                    (color_x + arrow_width//2, color_y + color_button_size//2 + 15 - arrow_height)   # Sağ alt köşe
                ])
            color_button_rect = pygame.Rect(
                color_x - color_button_size//2,
                color_y - color_button_size//2,
                color_button_size,
                color_button_size
            )
            
            # Buton fare üzerinde mi veya seçili mi kontrol et
            is_selected = (i == self.selected_color_index)
            is_hovered = color_button_rect.collidepoint(mouse_pos)
            
            # Butonu çiz - İç içe renkli çemberler
            border_color = YELLOW if is_selected or is_hovered else WHITE
            border_width = 3 if is_selected or is_hovered else 1
            
            # Dış çember - kenarlık
            pygame.draw.circle(
                self.screen, 
                border_color, 
                (color_x, color_y), 
                color_button_size//2 + 2, 
                border_width
            )
            
            # İç çember - renk örneği
            pygame.draw.circle(
                self.screen, 
                color_value, 
                (color_x, color_y), 
                color_button_size//2 - 2
            )
            
            # Eğer seçili renk ise, bir onay işareti göster
            if is_selected:
                # Kontrastlı renk seç (açık renklerde koyu, koyu renklerde açık işaret)
                check_color = (255, 255, 255) if sum(color_value) < 380 else (0, 0, 0)
                
                # Onay işareti (checkmark)
                check_points = [
                    (color_x - 15, color_y),                 # Başlangıç noktası
                    (color_x - 5, color_y + 10),             # Orta nokta
                    (color_x + 15, color_y - 10)             # Bitiş noktası
                ]
                pygame.draw.lines(self.screen, check_color, False, check_points, 3)
        
        # Geri butonu (ekranın alt kısmında)
        back_button_width, back_button_height = 200, 40
        back_button = pygame.Rect(
            SCREEN_WIDTH//2 - back_button_width//2,
            SCREEN_HEIGHT - 100,
            back_button_width,
            back_button_height
        )
        
        # Geri butonu fare üzerinde mi kontrol et
        is_back_hovered = back_button.collidepoint(mouse_pos)
        back_button_color = DARK_GREEN if is_back_hovered else (30, 50, 10)
        back_border_color = YELLOW if is_back_hovered else WHITE
        back_border_width = 3 if is_back_hovered else 1
        
        # Geri butonunu çiz
        pygame.draw.rect(self.screen, back_button_color, back_button, 0, 10)
        pygame.draw.rect(self.screen, back_border_color, back_button, back_border_width, 10)
        
        # Geri butonu metni
        back_text = self.font.render("GERİ", True, back_border_color)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Yönergeler
        info_box = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 50, 500, 30)
        # Kontrol tipine göre tuş bilgilerini güncelle
        if self.control_type == "arrow_keys":
            controls_text = self.small_font.render("Yukarı/Aşağı: Seçim   |   Enter: Onayla   |   Esc: Geri", True, WHITE)
        else:  # WASD kontrolleri
            controls_text = self.small_font.render("W/S: Seçim   |   Enter: Onayla   |   Esc: Geri", True, WHITE)
        controls_rect = controls_text.get_rect(center=info_box.center)
        self.screen.blit(controls_text, controls_rect)

    # Yüksek skoru kaydetme
    def save_high_score(self):
        try:
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))
        except:
            print("Yüksek skor kaydedilemedi")
            
    # Yüksek skoru yükleme
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except:
            # Dosya yoksa veya okunmazsa 0 döndür
            return 0
            
    def draw_game_over_screen(self):
        # Koyu arka plan
        game_over_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        game_over_overlay.fill((0, 0, 0, 200))  # Koyu saydam siyah
        self.screen.blit(game_over_overlay, (0, 0))
        
        # Daha büyük ve dikkat çekici OYUN BİTTİ yazısı
        game_over_text = self.title_font.render("OYUNU KAYBETTİNİZ", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        
        # Sarı renk ve daha büyük skor metni
        score_text = self.font.render(f"SKORUNUZ: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        
        # Yeni yüksek skor elde edildi mi kontrol et
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            high_score_text = self.small_font.render(f"YENİ REKOR!", True, ORANGE)
        else:
            high_score_text = self.small_font.render(f"En Yüksek Skor: {self.high_score}", True, WHITE)
        
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
        
        level_reached_text = self.small_font.render(f"Ulaşılan Seviye: {self.level + 1}", True, WHITE)
        level_reached_rect = level_reached_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
        # Sadece ana menü butonu için dikdörtgen
        button_width, button_height = 240, 50
        menu_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + 60, button_width, button_height)
        
        # Fare ile tıklama kontrolü
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        # Ana menü butonunu çiz
        menu_button_color = DARK_GREEN
        
        # Buton hover efekti
        if menu_button.collidepoint(mouse_pos):
            menu_button_color = (68, 95, 15)  # Daha açık yeşil (hover efekti)
            
        # Butonu çiz
        pygame.draw.rect(self.screen, menu_button_color, menu_button, 0, 10)  # Kenarları yuvarlatılmış buton
        
        # Buton kenarı
        pygame.draw.rect(self.screen, WHITE, menu_button, 2, 10)
        
        # Buton metni
        menu_text = self.font.render("ANA MENÜ", True, WHITE)
        menu_rect = menu_text.get_rect(center=menu_button.center)
        
        # Metinleri ekrana çiz
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(high_score_text, high_score_rect)
        self.screen.blit(level_reached_text, level_reached_rect)
        self.screen.blit(menu_text, menu_rect)
        
        # Ana menü butonuna tıklama işlemi
        if menu_button.collidepoint(mouse_pos) and mouse_click:
            self.reset_game()  # Önce oyunu sıfırla
            self.in_menu = True
            self.game_active = False  # Oyunu devre dışı bırak
            return  # İşlem tamamlandı, fonksiyondan çık

    def draw_pause_screen(self):
        pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 128))  # Yarı saydam siyah
        self.screen.blit(pause_overlay, (0, 0))
        
        pause_text = self.font.render("DURAKLADI", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        continue_text = self.small_font.render("Devam etmek için SPACE tuşuna basın", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        
        menu_text = self.small_font.render("Menüye dönmek için ESC tuşuna basın", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
        self.screen.blit(menu_text, menu_rect)
        
    def draw_level_up_message(self):
        # Seviye atlama mesajını göster
        level_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        level_overlay.fill((0, 0, 0, 100))  # Hafif saydam siyah
        self.screen.blit(level_overlay, (0, 0))
        
        # Seviye metni
        level_text = self.font.render(f"SEVİYE {self.level + 1}!", True, YELLOW)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        
        # Açıklama metni
        info_text = self.small_font.render("Yeni engeller eklendi!", True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        
        # Ekrana çizim
        self.screen.blit(level_text, level_rect)
        self.screen.blit(info_text, info_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

# Ana döngü
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

