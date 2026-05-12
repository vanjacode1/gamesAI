import './App.css'
import HomePage from './components/HomePage'
import { Routes, Route } from "react-router-dom"
import TicTacToePage from "./components/TicTacToePage"
import ConnectFourPage from "./components/ConnectFourPage"
import ChessPage from "./components/ChessPage"


function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/tic-tac-toe" element={<TicTacToePage />} />
      <Route path="/connect-four" element={<ConnectFourPage />} />
      <Route path="/chess" element={<ChessPage />} />
    </Routes>
  )
}

export default App
