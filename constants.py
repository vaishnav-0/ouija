BASE_PROMPT = (
    "Your response should be at most 3 words and should contain only letters and numbers. You can say yes "
    "to indicate affirmation and no to indicate negation. Your response should be spot on answer to the question and "
    "should not include any additional information.If asked about any person restrict your answer to most important "
    "term that describes the person."
)

ANGLE_MAX = 925


LETTER_MAP = {
    "A": (3800, 95),
    "B": (3900, 180),
    "C": (4000, 270),
    "D": (4100, 340),
    "E": (4200, 400),
    "F": (4200, 450),
    "G": (4150, 520),
    "H": (4170, 600),
    "I": (4170, 650),
    "J": (4150, 710),
    "K": (4090, 790),
    "L": (4090, 860),
    "M": (3800, 0),
    "N": (500, 920),
    "O": (510, 850),
    "P": (530, 770),
    "Q": (530, 700),
    "R": (530, 610),
    "S": (520, 530),
    "T": (490, 460),
    "U": (450, 370),
    "V": (420, 270),
    "W": (400, 200),
    "X": (360, 115),
    "Y": (300, 60),
    "Z": (100, 20),
    "1": (1, 0),
    "2": (1, 1),
    "3": (1, 2),
    "4": (1, 3),
    "5": (1, 4),
    "6": (1, 5),
    "7": (1, 6),
    "8": (1, 7),
    "9": (1, 8),
    "0": (1, 9),
    "YES": (2, 0),
    "NO": (2, 1),
    "CENTER": (4300//2, 0)
}
