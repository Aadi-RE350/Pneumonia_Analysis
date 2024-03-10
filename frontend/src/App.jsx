import { useState } from 'react'
import Home_page from './home_page'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Home_page/>
    </>
  )
}

export default App
