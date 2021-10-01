import React from 'react'
import Nav from './components/NavBar'
import Login from './views/Login'
import HomePage from './views/HomePage'
import Signup from './views/Signup'
import Product from './views/ProductAdd'
import ItemPage from './views/ItemPage'
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
            <Route path="/product" exact component={Product} />
            <Route path="/item" exact component={ItemPage} />
          </Switch>
      </div>
    </Router>
  );
}

export default App;
