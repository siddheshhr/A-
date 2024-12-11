import { useState } from 'react'
import {Button} from 'flowbite-react';
import NavBarTop from './components/NavBarTop';
import MapContent from './components/MapContent';
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <NavBarTop/>
      <MapContent/>
    </>
  )
}

export default App
