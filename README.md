<!-- Edite o arquivo "jigsaw.py", mais especificamente a função "solve"
A classe "jigsaw" tem referência a todas as peças do quebra cabeça, todas as peças estão classificadas com os três tipos possíveis.
As peças tem informação sobre os 4 cantos, e cada canto possui informação sobre seu tipo e sobre seu contorno (que é um conjunto de pontos)
A funçao "solve" deve utilizar essas informações disponíveis para resolver o quebra cabeça, pode retornar a solução do jeito que achar melhor,
podemos arrumar esse output depois. -->

Great! Now I need to implement the solve method, to solve the jigsaw puzzle, using the self.pieces list attribute.

self.pieces is a list of Pieces Objects, which has attributes such as:

- center (the center coordinates of the piece)
- image (the image array of the piece)
- type: the type of the piece, which is an Enum with three possible values: BORDER, CORNER, CENTER, defined as follows:

```python
class PieceType(Enum):
    BORDER = 0
    CORNER = 1
    CENTER = 2
```

- most importantly, sides, which is a List of "Side" objects, defined as follows:

```python
class SideType(Enum):
    HEAD = 0
    HOLE = 1
    FLAT = 2


class SidePosition(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Side:

    def __init__(self, points: np.ndarray, type: SideType):
        self.points = points
        self.length = cv2.arcLength(points, False)
        self.type = type

        M = cv2.moments(self.points)
        self.center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]

        self.can_attach_piece = self.type != SideType.FLAT
        self.position = None

    def attach_piece(self):
        self.can_attach_piece = False

    def set_position(self, position: SidePosition):
        self.position = position

```

Considering that, I want you to create the solve method that:

- Create the Board. The board will be an array of arrays containing Pieces, where each sub-array is a row of the jigsaw board. Based on the lenght of the pieces and the number of flat sides, identify the number of rows and columns of the board, and create an empty board. Also, create a list of pieces that are not yet placed on the board (pieces_to_place).

- Identify one corner from the pieces, and place it on the top left corner of the board. This will be the first piece of the board (removes it from the list of pieces to place). For each side, use the set_position method to set the position of the side on the piece. One FLAT side must be on the left, and the other on the top. Beacause "sides" are in order to complete the piece, the fist side identified as FLAT must be on the left, the second on the top, and the subsequent sides must be right and bottom (even if you need to return to the index 0 again to find the subsequent side).

- Create a function that receives two side points, and returns a coefficient of match. This will be used to identify which head will be attached to each hole.

- After that, I want to create the frame, which means all the pieces with FLAT side types on the board (creating the jigsaw border), using the matching function created. Beggining from the top left corner, start placing the pieces on the board clockwise, starting connecting a piece with the left side of the top left piece. Use the following logic:

1. Filter the pieces candidates from the pieces_to_place: if the side that will recieve the piece is a HOLE, the piece must have a HEAD side to connect (can_attach_piece = True and type = HEAD). If the side that will recieve the piece is a HEAD, the piece must have a HOLE side to connect (can_attach_piece = True and type = HOLE). Also, as we are creating the frame, the piece must have a FLAT side.
2. For each candidate piece, calculate the match coefficient with the piece that is already on the board. The match coefficient is calculated by the function created before, and the best match is the one with the highest coefficient. Every piece attached to the board must have the attach_piece method called on the side that was attached. Also, all the sides of the piece must have the set_position method called.
3. After the first row is complete, as we are creating the frame, clockwise, the pieces attached will be from the right corner, to the bottom corner, to finally the left corner to complete the frame.
