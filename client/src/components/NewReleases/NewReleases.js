import SpotifyWebApi from 'spotify-web-api-js';
import React, {Component} from 'react';

const spotifyApi = new SpotifyWebApi();

export default class NewReleases extends Component {
    constructor() {
        super();
        this.state = {
            results: [],
            prev: null,
            next: null
        }
    };

    getNewReleases = (e, url) => {
        if (url === undefined) {
            url = 'http://localhost:8000/get-new-music-friday-no-rap';
        }
        fetch(url)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                debugger
                this.setState({results: []});
                this.setState({
                    results: data,
                })
            })
    };

    render() {
        return (
            <div className="App">

                <button onClick={this.getNewReleases}>Get New Releases</button>

                <table>
                    <caption>New Releases</caption>
                    <tbody>
                    {
                        this.state.results.length > 1 &&
                        this.state.results.map((track, i) => {
                            return <tr key={i}>

                                <td> {track.name}</td>
                                <td> {track.artists.map((artist) => artist.name).join(', ')}</td>

                                <td>
                                    <a href={track.external_urls.spotify} target="_blank">Play</a>
                                </td>
                            </tr>
                        })
                    }
                    </tbody>
                </table>
                <div>
                    {this.state.prev && <button onClick={(e) => this.getNewReleases(e, this.state.prev)}>Previous</button>}
                    {this.state.next && <button onClick={(e) => this.getNewReleases(e, this.state.next)}>Next</button>}
                </div>
            </div>
        );
    }
}