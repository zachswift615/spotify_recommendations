import React, {Component} from 'react';
import {Switch, Route, BrowserRouter} from "react-router-dom";
import Login from "../Login/Login";
import HomePage from "../HomePage/HomePage";
import WorkoutDetail from '../WorkoutDetail/WorkoutDetail';
import WorkoutCard from "../WorkoutCard/WorkoutCard";


class Router extends Component {
  render() {
    return (
        <BrowserRouter>
          <Switch>
            <Route exact path="/login" component={Login}/>
            <Route exact path="/" component={HomePage}/>
            <Route exact path="/workout/:workout_id" render={(props) => {
              return <WorkoutDetail workout_id={props.match.params.workout_id}/>
            }}/>
          </Switch>
        </BrowserRouter>
    );
  }
}

export default Router;
