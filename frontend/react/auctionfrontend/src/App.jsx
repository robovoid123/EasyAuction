import React from 'react'
import Nav from './components/NavBar'
import Login from './views/Login'
import HomePage from './views/HomePage'
import Signup from './views/Signup'
import Auction from './views/AuctionManagement'
import AuctionAdd from './views/AuctionAdd'
import {AuctionUpdate} from './views/AuctionUpdate'
import ItemPage from './views/ItemPage'
import SearchResult from './views/SearchResult'
import BidItemList from './views/BidItemList'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'


function App() {
  return (
    <Router>
      <div className="App">
          <Nav />
          <Switch>
            <Route path="/" exact component={HomePage} />
            <Route path="/login" exact component={Login} />
            <Route path="/signup" exact component={Signup} />
            <Route path="/product" exact component={Auction} />
            <Route path="/productAdd" exact component={AuctionAdd} />
            <Route path="/productUpdate" exact component={AuctionUpdate} />
            <Route path="/biditemlist" exact component={BidItemList} />
            <Route path="/item" exact component={ItemPage} />
            <Route path="/searchResult" exact component={SearchResult} />
          </Switch>
      </div>
    </Router>
  );
}

export default App;
