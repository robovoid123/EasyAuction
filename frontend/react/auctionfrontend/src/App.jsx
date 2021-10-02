import React from 'react'
import Nav from './components/NavBar'
import Login from './views/Login'
import HomePage from './views/HomePage'
import Signup from './views/Signup'
import Product from './views/ProductManagement'
import ProductAdd from './views/ProductAdd'
import {ProductUpdate} from './views/ProductUpdate'
import ItemPage from './views/ItemPage'
import SearchResult from './views/SearchResult'
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
            <Route path="/productAdd" exact component={ProductAdd} />
            <Route path="/productUpdate" exact component={ProductUpdate} />
            <Route path="/item" exact component={ItemPage} />
            <Route path="/searchResult" exact component={SearchResult} />
          </Switch>
      </div>
    </Router>
  );
}

export default App;
