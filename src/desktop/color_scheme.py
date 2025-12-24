import pygame


class ColorScheme:
    def __init__(self):
        self.colors = {
            'i': pygame.Color(255, 0, 0),
            'j': pygame.Color(0, 0, 255),
            'l': pygame.Color(255, 172, 0),
            'o': pygame.Color(255, 255, 0),
            's': pygame.Color(0, 255, 255),
            't': pygame.Color(255, 0, 255),
            'z': pygame.Color(0, 255, 0),
        }

    def cellColor(self, aChar, isPaused, currentPiece):
        isGhost = False

        if aChar == '#':
            aChar = currentPiece
            isGhost = True

        if aChar in self.colors.keys():
            color = self.colors[aChar]
            if isGhost:
                color = pygame.Color(color.r // 5, color.g // 5, color.b // 5)
            if isPaused:
                return color.grayscale()
            return color
        return pygame.Color(0, 0, 0)
