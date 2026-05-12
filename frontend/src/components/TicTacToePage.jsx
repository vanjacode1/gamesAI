import { useState } from "react"
import axios from "axios"
import "../styles/TicTacToePage.css"

function TicTacToePage() {
  const [board, setBoard] = useState([
    [null, null, null],
    [null, null, null],
    [null, null, null],
  ])

  const [isAiThinking, setIsAiThinking] = useState(false)
  const [showAiThinkingMessage, setShowAiThinkingMessage] = useState(false)
  const [gameResult, setGameResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)

  const humanPlayer = "X"
  const aiPlayer = "O"
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

  async function askAiMove(currentBoard) {

    setIsAiThinking(true)
    setShowAiThinkingMessage(false)

    // delay showing AI is thinking message by 10ms
    // if backend response takes longer than 10ms show that AI is thinking
    const thinkingTimer = setTimeout(() => {
        setShowAiThinkingMessage(true)
    }, 10)
    
    try {
        const response = await axios.post(`${API_BASE_URL}/api/tictactoe-move`, {
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

    async function handleSquareClick(rowIndex, columnIndex) {
        // ignore user move if AI is thinking of a move, game is finished, square is filled
        if (isAiThinking) return
        if (gameResult !== null) return
        if (board[rowIndex][columnIndex] !== null) return


        const newBoard = board.map((row) => [...row])
        newBoard[rowIndex][columnIndex] = humanPlayer

        setBoard(newBoard)

        await askAiMove(newBoard)
        
  }

    function startNewGame() {
      setBoard([
        [null, null, null],
        [null, null, null],
        [null, null, null],
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
        <h1 className="landing-title">Tic Tac Toe</h1>

        <p className="game-status">{getStatusText()}</p>

        <div className="board">
          {board.map((row, rowIndex) => (
            <div className="board-row" key={rowIndex}>
              {row.map((cell, colIndex) => (
                <button
                  className="square"
                  key={`${rowIndex}-${colIndex}`}
                  onClick={() => handleSquareClick(rowIndex, colIndex)}
                >
                  {cell}
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

export default TicTacToePage