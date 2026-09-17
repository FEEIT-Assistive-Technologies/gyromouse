import pygame
import math
import statistics
import random
import pyautogui

# ----------------------------
# Settings
# ----------------------------
WIDTH, HEIGHT = 1000, 700
TARGET_RADIUS = 11
CLICK_RADIUS = 2
NUM_CLICKS = 35

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Accuracy & Precision Test")

font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

target = (WIDTH // 2, HEIGHT // 2)
clicks = []

screen_width, screen_height = pyautogui.size()

import time


class ConsoleStopwatch:
    def __init__(self):
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.laps = []

    def get_elapsed(self):
        if self.running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 100)
        return f"{mins:02d}:{secs:02d}:{millis:02d}"

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            print("\n[Stopwatch Started]")

    def stop(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            print(f"\n[Stopwatch Paused] Current Time: {self.format_time(self.get_elapsed())}")

    def lap(self):
        current_time = self.get_elapsed()
        if current_time > 0:
            lap_time_str = self.format_time(current_time)
            self.laps.append(lap_time_str)
            print(f"\n[Lap {len(self.laps):02d}] Recorded: {lap_time_str}")
        else:
            print("\n[Stopwatch hasn't started yet]")

    def reset(self):
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.laps.clear()
        print("\n[Stopwatch Reset]")

    def show_laps(self):
        if not self.laps:
            print("\nNo laps recorded yet.")
        else:
            print("\n--- Lap History ---")
            for i, lap in enumerate(self.laps, 1):
                print(f"Lap {i:02d} — {lap}")

    def run(self):
        print("=== Console Stopwatch with Laps ===")
        while True:
            current_str = self.format_time(self.get_elapsed())
            print(f"\nCurrent Time: {current_str} {'(Running)' if self.running else '(Paused)'}")
            print("1. Start  2. Stop  3. Lap  4. Show Laps  5. Reset  6. Exit")

            choice = input("Enter choice (1-6): ").strip()

            if choice == '1':
                self.start()
            elif choice == '2':
                self.stop()
            elif choice == '3':
                self.lap()
            elif choice == '4':
                self.show_laps()
            elif choice == '5':
                self.reset()
            elif choice == '6':
                print("\nExiting stopwatch. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please select between 1 and 6.")

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


running = True

stopwatch = ConsoleStopwatch()
stopwatch.start()

while running:
    screen.fill((245, 245, 245))

    # Draw target
    pygame.draw.circle(screen, (255, 0, 0), target, TARGET_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), target, TARGET_RADIUS + 2, 1)

    # Draw clicks
    for c in clicks:
        pygame.draw.circle(screen, (0, 100, 255), c, CLICK_RADIUS)

    txt = font.render(
        f"Click the target ({len(clicks)}/{NUM_CLICKS})",
        True,
        (0, 0, 0),
    )
    screen.blit(txt, (20, 20))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(clicks) < NUM_CLICKS:
                clicks.append(event.pos)
                # Generate random X and Y coordinates within screen boundaries
                random_x = random.randint(0, screen_width - 1)
                random_y = random.randint(0, screen_height - 1)

                # Move the cursor to the random location
                pyautogui.moveTo(random_x, random_y)

                stopwatch.lap()

    if len(clicks) == NUM_CLICKS:
        running = False

    clock.tick(120)

pygame.quit()

# ----------------------------
# Calculations
# ----------------------------

xs = [p[0] for p in clicks]
ys = [p[1] for p in clicks]

mean_x = statistics.mean(xs)
mean_y = statistics.mean(ys)
mean_point = (mean_x, mean_y)

# Accuracy
accuracy_error = distance(mean_point, target)

# Precision (RMS spread)
precision = math.sqrt(
    sum(
        (x - mean_x) ** 2 + (y - mean_y) ** 2
        for x, y in clicks
    ) / len(clicks)
)

# Radial errors
errors = [distance(c, target) for c in clicks]

mean_radial_error = statistics.mean(errors)
max_error = max(errors)

# CEP50 and CEP95
sorted_errors = sorted(errors)

cep50 = sorted_errors[int(0.50 * len(sorted_errors))]
cep95 = sorted_errors[min(int(0.95 * len(sorted_errors)), len(sorted_errors)-1)]

# ----------------------------
# Results
# ----------------------------

print("\n========== RESULTS ==========")
print(f"Target            : {target}")
print(f"Average Click     : ({mean_x:.2f}, {mean_y:.2f})")
print(f"Accuracy Error    : {accuracy_error:.2f} px")
print(f"Precision (RMS)   : {precision:.2f} px")
print(f"Mean Radial Error : {mean_radial_error:.2f} px")
print(f"CEP50             : {cep50:.2f} px")
print(f"CEP95             : {cep95:.2f} px")
print(f"Maximum Error     : {max_error:.2f} px")
print("=============================\n")

stopwatch.stop()
stopwatch.show_laps()