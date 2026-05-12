import { useState } from "react"
import axios from "axios"
import "../styles/ConnectFourPage.css"

function ConnectFourPage() {

  const [board, setBoard] = useState([
    [null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null],
  ])

  const [isAiThinking, setIsAiThinking] = useState(false)
  const [showAiThinkingMessage, setShowAiThinkingMessage] = useState(false)
  const [gameResult, setGameResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)

  const humanPlayer = "R"
  const aiPlayer = "Y"

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

  function getLowestEmptyRow(board, col) {
  for (let row = 5; row >= 0; row--) {
    if (board[row][col] === null) {
      return row
    }
  }

  return null
}

  async function askAiMove(currentBoard) {

    setIsAiThinking(true)
    setShowAiThinkingMessage(false)

    // delay showing AI is thinking message by 10ms
    // if backend response takes longer than 10ms show that AI is thinking
    const thinkingTimer = setTimeout(() => {
        setShowAiThinkingMessage(true)
    }, 10)
    
    try {
        const response = await axios.post(`${API_BASE_URL}/api/connectfour-move`, {
            board: currentBoard,
            ai_player: aiPlayer,
            human_player: humanPlayer,
        })

        const { winner, board: updatedBoard } = response.data

        setBoard(updatedBoard)

        if (winner !== null) {
            setGameResult(winner)
        }
    } catch (error) {
        setErrorMessage("Something went wrong. Please try again.")
    } finally {
        clearTimeout(thinkingTimer)
        setIsAiThinking(false)
        setShowAiThinkingMessage(false)
    }
  }

  async function handleColumnClick(col) {
        if (isAiThinking) return
        if (gameResult !== null) return

        const row = getLowestEmptyRow(board, col)

        if (row === null) return

        const newBoard = board.map((row) => [...row])
        newBoard[row][col] = humanPlayer

        setBoard(newBoard)

        await askAiMove(newBoard)
    }

    function startNewGame() {
        setBoard([
            [null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null],
        ])

      setGameResult(null)
      setIsAiThinking(false)
      setErrorMessage(null)
    }

  function getStatusText() {
    if (errorMessage) return errorMessage
    if (gameResult === humanPlayer) return "You won!"
    if (gameResult === aiPlayer) return "AI won!"
    if (gameResult === "draw") return "It's a draw!"
    if (showAiThinkingMessage) return "AI is thinking..."
    return "Your turn"
  }

return (
  <div className="landing-page">
    <div className="landing-content">
      <h1 className="landing-title">Connect Four</h1>

      <p className="game-status">{getStatusText()}</p>

      <div className="connect-four-board">
        {board.map((row, rowIndex) => (
          <div className="connect-four-row" key={rowIndex}>
            {row.map((cell, colIndex) => (
              <button
                key={`${rowIndex}-${colIndex}`}
                className={`connect-four-cell ${
                  cell === "R"
                    ? "red-piece"
                    : cell === "Y"
                    ? "yellow-piece"
                    : "empty-cell"
                }`}
                onClick={() => handleColumnClick(colIndex)}
              >
              </button>
            ))}
          </div>
        ))}
      </div>

      <div className="game-controls">
        <button className="retro-button" onClick={startNewGame}>
          New Game
        </button>
      </div>
    </div>
  </div>
)
}

export default ConnectFourPage