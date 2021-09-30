import React, { useEffect, useState } from 'react'

import './assets/css/style.css';
import AuctionShowCase from './components/AuctionShowCase/AuctionShowCase';
import Navbar from './components/Navbar/Navbar';

const App = () => {
  const [auctions, setAuctions] = useState([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/auctions/?skip=0&limit=5', { mode: 'cors' })
      .then((response) => response.json())
      .then((json) => {
        console.log(json)
        setAuctions(json)
      });
  }, [])

  return (
    <div>
      <Navbar />
      <AuctionShowCase auctions={auctions} />
    </div>
  )
}

export default App



