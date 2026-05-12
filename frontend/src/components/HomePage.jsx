import "../styles/HomePage.css"
import { useNavigate } from "react-router-dom" 

function HomePage() {

    const navigate = useNavigate();


    function chooseGame(game) {
        if (game === "tic-tac-toe") {
            navigate("/tic-tac-toe");
        }

        if (game === "connect-four") {
            navigate("/connect-four");
        }

        if (game === "chess") {
            navigate("/chess");
        }
    }

  return (
    <div className="landing-page">
      <div className="landing-content">
        <h1 className="landing-title">
          <span>Play classic games</span>
          <span>against an AI opponent</span>
        </h1>

        <p className="landing-description">
          Challenge an LLM in simple strategy games. You make a move, the backend
          validates the rules, and the AI responds with its own move. Or play chess against a chess engine were an LLM assists you while playing.
        </p>

        <div className="landing-buttons">
          <button onClick={() => chooseGame("tic-tac-toe")} className="retro-button">Tic Tac Toe</button>
          <button onClick={() => chooseGame("connect-four")} className="retro-button">Connect Four</button>
          <button onClick={() => chooseGame("chess")} className="retro-button">Chess</button>
        </div>
      </div>
    </div>
  )
}

export default HomePage