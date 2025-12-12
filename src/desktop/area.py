import pygame


class Area:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def asRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def withPadding(self, paddingX, paddingY):
        return Area(
            self.x + paddingX,
            self.y + paddingY,
            self.width - paddingX * 2,
            self.height - paddingY * 2
        )

    def centeredAt(self, anArea):
        return Area(
            (anArea.width - self.width) / 2,
            (anArea.height - self.height) / 2,
            self.width,
            self.height
        )
