import SpotifyWebApi from 'spotify-web-api-js';
import React, {Component} from 'react';
import "./SearchResults.css";

const spotifyApi = new SpotifyWebApi();

export default class SearchResults extends Component {
    constructor() {
        super();
    };

    render() {
        return (
            <div className="App">

                <table>
                    <caption>{this.props.caption}</caption>
                    <tbody>
                    {
                        this.props.trackSearchResults.length > 1 && !this.props.songFeatures &&
                        this.props.trackSearchResults.map((track, i) => {
                            const imgObj = track.album.images.filter(imgObj => imgObj.height === 64)[0];
                            return <tr key={i}>
                                <td><img src={track.album.images.sort((a, b) => a.height - b.height)[0].url} alt=""/>
                                </td>
                                <td> {track.name}</td>
                                <td> {track.artists.map((artist) => artist.name).join(', ')}</td>
                                <td>
                                    <button onClick={() => this.props.getAudioFeatures(track.id)}>Get Audio Features
                                    </button>
                                </td>
                                <td>
                                    <button onClick={() => this.props.addToSeedTracks(track)}>Use as seed track
                                    </button>
                                </td>
                                <td>
                                    <a target="_blank" href={track.external_urls.spotify}>Play</a>
                                </td>
                            </tr>
                        })
                    }
                    </tbody>
                </table>
            </div>
        );
    }
}