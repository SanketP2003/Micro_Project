import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Tool from './components/Tool'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Tool />} />
      </Routes>
    </div>
  )
}

export default App
