CONNECT_FOUR_PROMPT = """
We are playing Connect Four.

The board is a 6x7 grid with coordinates:
- Rows are numbered from 0 to 5.
- Row 0 is the top row.
- Row 5 is the bottom row.
- Columns are numbered from 0 to 6, from left to right.

The board contains:
- "R"
- "Y"
- null for empty cells

You must choose exactly one move from the available moves list that will be provided.

Your goal is to connect 4 of your pieces horizontally, vertically, or diagonally.
You should also block the opponent when they are close to connecting 4 pieces.

Do not choose a full column.
Do not explain your answer.
"""