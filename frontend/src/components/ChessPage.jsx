import { useState } from "react"
import axios from "axios"
import { Chess } from "chess.js"
import { Chessboard } from "react-chessboard"
import "../styles/ChessPage.css"

function ChessPage() {
  const [game, setGame] = useState(new Chess())
  const [isEngineThinking, setIsEngineThinking] = useState(false)
  const [gameStatus, setGameStatus] = useState("ongoing")
  const [winner, setWinner] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)

  const [playerMoveAnalysis, setPlayerMoveAnalysis] = useState(null)
  const [engineMoveAnalysis, setEngineMoveAnalysis] = useState(null)
  const [positionSummary, setPositionSummary] = useState(null)

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

  async function sendMoveToBackend({ fenBefore, playerMove }) {
    setIsEngineThinking(true)
    setErrorMessage(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chess-move`, {
        fen_before: fenBefore,
        player_move: {
          from_square: playerMove.from,
          to_square: playerMove.to,
          promotion: playerMove.promotion || null,
        },
      })

      const {
        fen,
        status,
        winner,
        player_move_analysis,
        engine_move_analysis,
        position_summary,
      } = response.data

      setGame(new Chess(fen))
      setGameStatus(status)
      setWinner(winner)

      setPlayerMoveAnalysis(player_move_analysis)
      setEngineMoveAnalysis(engine_move_analysis)
      setPositionSummary(position_summary)
    } catch (error) {
      console.error(error)
      setGame(new Chess(fenBefore))
      setErrorMessage("Something went wrong. Please try again.")
    } finally {
      setIsEngineThinking(false)
    }
  }

  function onDrop({ sourceSquare, targetSquare }) {
    if (isEngineThinking) return false
    if (winner !== null) return false
    if (gameStatus === "checkmate" || gameStatus === "draw") return false

    const fenBefore = game.fen()
    const gameCopy = new Chess(fenBefore)

    const move = gameCopy.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q",
    })

    if (move === null) {
      return false
    }

    setGame(gameCopy)

    sendMoveToBackend({
      fenBefore,
      playerMove: move,
    })

    return true
  }

  function startNewGame() {
    setGame(new Chess())
    setIsEngineThinking(false)
    setGameStatus("ongoing")
    setWinner(null)
    setErrorMessage(null)

    setPlayerMoveAnalysis(null)
    setEngineMoveAnalysis(null)
    setPositionSummary(null)
  }

  function getStatusText() {
    if (errorMessage) return errorMessage
    if (winner === "player") return "You won!"
    if (winner === "engine") return "Engine won!"
    if (gameStatus === "draw") return "It's a draw!"
    if (isEngineThinking) return "Engine is thinking..."
    return "Your move"
  }

  const chessboardOptions = {
    position: game.fen(),
    onPieceDrop: onDrop,

    darkSquareStyle: {
      backgroundColor: "#2e4988",
    },

    lightSquareStyle: {
      backgroundColor: "#22c55e",
    },
  }

  return (
  <div className="chess-page">
    <div className="chess-layout">
      <section className="chess-left">
        <h1 className="chess-title">Chess Coach</h1>

        <p className="game-status">{getStatusText()}</p>

        <div className="chess-board-frame">
          <Chessboard options={chessboardOptions} />
        </div>

        <div className="game-controls">
          <button className="retro-button" onClick={startNewGame}>
            New Game
          </button>
        </div>
      </section>

      <aside className="chess-analysis-panel">
        <h2>Analysis</h2>

        {!playerMoveAnalysis && !engineMoveAnalysis && !positionSummary && (
          <p className="analysis-placeholder">
            Make a move to get AI commentary.
          </p>
        )}

        {playerMoveAnalysis && (
          <div className="analysis-card">
            <h3>Your move</h3>
            <p>{playerMoveAnalysis}</p>
          </div>
        )}

        {engineMoveAnalysis && (
          <div className="analysis-card">
            <h3>Engine move</h3>
            <p>{engineMoveAnalysis}</p>
          </div>
        )}

        {positionSummary && (
          <div className="analysis-card">
            <h3>Position</h3>
            <p>{positionSummary}</p>
          </div>
        )}
      </aside>
    </div>
  </div>
)
}

export default ChessPage