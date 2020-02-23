import React, {Component} from 'react';
import {Switch, Route, BrowserRouter} from "react-router-dom";
import NewReleases from "./components/NewReleases/NewReleases";
import App from "./App";

class Router extends Component {
  render() {
    return (
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={App}/>
            <Route exact path="/new-releases" component={NewReleases}/>
          </Switch>
        </BrowserRouter>
    );
  }
}

export default Router;
