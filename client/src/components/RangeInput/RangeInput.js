import React, { Component } from 'react';
import { Range } from 'rc-slider';
import '../../../node_modules/rc-slider/assets/index.css';
import "./RangeInput.css"

export default class RangeInput extends Component {

  constructor(props) {
    super(props);
    this.inputChanged = this.inputChanged.bind(this);
  }

  inputChanged(response) {
    this.props.onChange(response[0], response[1]);
  }

  render() {

    return (
      <div className={'range-container'}>
        <label>
          {this.props.label}
        </label>
        <Range
          min={this.props.min}
          max={this.props.max}
          allowCross={false}
          defaultValue={[
            this.props.initMin,
            this.props.initMax,
          ]}
          railStyle={{
            height: '2px',
          }}
          step={this.props.step}
          onAfterChange={this.inputChanged}
        />
        <div >
          <b>{this.props.minLabel}</b>
          <b className={'max-label'}>{this.props.maxLabel}</b>
        </div>
      </div>
    );
  }
}
