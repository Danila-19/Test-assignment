import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


class CityGrid:
    def __init__(self, rows, cols, obstacle_percentage=30):
        self.rows = rows
        self.cols = cols
        self.obstacle_percentage = obstacle_percentage
        self.grid = self.generate_grid()

    def generate_grid(self):
        grid = np.zeros((self.rows, self.cols), dtype=int)

        num_obstacles = int((self.obstacle_percentage / 100) *
                            (self.rows * self.cols))
        obstacle_positions = np.random.choice(
            self.rows * self.cols, num_obstacles, replace=False
        )
        obstacle_rows, obstacle_cols = np.unravel_index(
            obstacle_positions, (self.rows, self.cols)
        )
        grid[obstacle_rows, obstacle_cols] = 1

        return grid

    def visualize_grid(self):
        fig, ax = plt.subplots()
        for i in range(self.rows + 1):
            ax.plot([0, self.cols], [i, i], color='black', linewidth=1)

        for j in range(self.cols + 1):
            ax.plot([j, j], [0, self.rows], color='black', linewidth=1)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    rect = Rectangle((j, i), 1, 1, color='black')
                    ax.add_patch(rect)

        ax.set_aspect('equal', 'box')
        plt.xlim(0, self.cols)
        plt.ylim(0, self.rows)
        plt.title('Город с препятствиями')
        plt.show()

    def place_tower(self, row, col):
        self.grid[row, col] = 2
        self.update_coverage(row, col)

    def update_coverage(self, row, col):
        radius = 1
        for i in range(max(0, row - radius), min(self.rows, row + radius + 1)):
            for j in range(max(0, col - radius),
                           min(self.cols, col + radius + 1)):
                if self.grid[i, j] == 0:
                    self.grid[i, j] = 3

    def visualize_tower_coverage(self):
        fig, ax = plt.subplots()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    rect = Rectangle((j, i), 1, 1, color='black')
                    ax.add_patch(rect)
                elif self.grid[i, j] == 2:
                    circle = Circle((j + 0.5, i + 0.5), 0.1, color='red')
                    ax.add_patch(circle)
                elif self.grid[i, j] == 3:
                    rect = Rectangle((j, i), 1, 1, color='green', alpha=0.5)
                    ax.add_patch(rect)

        ax.set_aspect('equal', 'box')
        plt.xlim(0, self.cols)
        plt.ylim(0, self.rows)
        plt.title('Покрытие вышки')
        plt.show()

    def optimize_tower_placement_with_budget(self, tower_cost, budget):
        clear_blocks = np.argwhere(self.grid == 0)

        tower_positions = np.argwhere(self.grid == 2)
        tower_coverage = [
            np.sum(
                self.grid[
                    max(0, row - 1): min(self.rows, row + 2),
                    max(0, col - 1): min(self.cols, col + 2),
                ]
                == 3
            )
            for row, col in tower_positions
        ]

        while len(clear_blocks) > 0 and budget >= tower_cost:
            max_coverage_per_cost = 0
            selected_block = None

            for block in clear_blocks:
                row, col = block[0], block[1]
                block_coverage = np.sum(
                    self.grid[
                        max(0, row - 1): min(self.rows, row + 2),
                        max(0, col - 1): min(self.cols, col + 2),
                    ]
                    == 0
                )

                for i, tower_pos in enumerate(tower_positions):
                    dist = np.sqrt(
                        (row - tower_pos[0]) ** 2 + (col - tower_pos[1]) ** 2
                    )
                    block_coverage -= min(tower_coverage[i],
                                          block_coverage / dist)

                coverage_per_cost = block_coverage / tower_cost

                if coverage_per_cost > max_coverage_per_cost:
                    max_coverage_per_cost = coverage_per_cost
                    selected_block = block

            if selected_block is not None:
                row, col = selected_block[0], selected_block[1]
                self.place_tower(row, col)
                budget -= tower_cost

            clear_blocks = np.argwhere(self.grid == 0)

        return budget

    def visualize_tower_placement(self):
        fig, ax = plt.subplots()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    rect = Rectangle((j, i), 1, 1, color='black')
                    ax.add_patch(rect)
                elif self.grid[i, j] == 2:
                    circle = Circle((j + 0.5, i + 0.5), 0.1, color='red')
                    ax.add_patch(circle)
                elif self.grid[i, j] == 3:
                    rect = Rectangle((j, i), 1, 1, color='green', alpha=0.5)
                    ax.add_patch(rect)

        ax.set_aspect('equal', 'box')
        plt.xlim(0, self.cols)
        plt.ylim(0, self.rows)
        plt.title('Покрытие вышками изходя из бюджета')
        plt.show()


if __name__ == "__main__":
    tower_cost = 10
    budget = 50

    city = CityGrid(rows=10, cols=10, obstacle_percentage=30)
    city.visualize_grid()

    city.place_tower(row=5, col=5)
    city.visualize_tower_coverage()

    remaining_budget = city.optimize_tower_placement_with_budget(tower_cost,
                                                                 budget)
    print(f"Remaining budget: {remaining_budget}")

    city.visualize_tower_placement()
