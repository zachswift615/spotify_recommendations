import React, {Component} from 'react';


export default class SongFeatures extends Component {

    render() {
        return (
            <div className="">
                <table>
                    <tbody>
                    {
                        Object.keys(this.props.songFeatures).map((key, i) => {
                            return <tr key={i}>
                                <td>{key}</td>
                                <td>{this.props.songFeatures[key]}</td>
                            </tr>
                        })
                    }
                    </tbody>
                </table>
            </div>
        );
    }
}