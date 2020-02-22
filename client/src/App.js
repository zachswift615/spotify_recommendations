import SpotifyWebApi from 'spotify-web-api-js';
import React, {Component} from 'react';
import "./App.css";
import SearchResults from "./components/SearchResults/SearchResults";
import SongFeatures from "./components/SongFeatures/SongFeatures";
import SeedTracksList from "./components/SeedTracksList/SeedTracksList";
import { faTimes } from '@fortawesome/free-solid-svg-icons'

import MetaTags from 'react-meta-tags';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const spotifyApi = new SpotifyWebApi();

export default class App extends Component {
    constructor() {
        super();
        const params = this.getHashParams();
        const token = params.access_token;
        if (token) {
            spotifyApi.setAccessToken(token);
        }
        this.state = {
            loggedIn: !!token,
            nowPlaying: {name: 'Not Checked', albumArt: ''},
            query: "",
            trackSearchResults: [],
            songAnalasys: {},
            songFeatures: {},
            songRecommendations: [],
            seedTracks: []
        }
    };

    getHashParams = () => {
        var hashParams = {};
        var e, r = /([^&;=]+)=?([^&;]*)/g,
            q = window.location.hash.substring(1);
        e = r.exec(q);
        while (e) {
            hashParams[e[1]] = decodeURIComponent(e[2]);
            e = r.exec(q);
        }
        return hashParams;
    };

    onSearchInputChange = (event) => {
        this.setState({
            query: event.currentTarget.value
        })

    };

    addToSeedTracks = (trackToAdd) => {
        let songSeedsCopy = [...this.state.seedTracks];
        let match = songSeedsCopy.filter(track => track.id === trackToAdd.id);
        if (!match.length > 0) {
            songSeedsCopy.push(trackToAdd);
            this.setState({seedTracks: songSeedsCopy})
        }
    };

    resetDetails = () => {
        this.setState({
            songFeatures: null,
            songAnalasys: null,
        })
    };

    removeFromSeedTracks = (trackToRemove) => {
        let seedTracksCopy = [...this.state.seedTracks];
        seedTracksCopy = seedTracksCopy.filter((track) => track.id !== trackToRemove.id);
        this.setState({seedTracks: seedTracksCopy})
    };

    clearSearchResults = () => {
        this.setState({trackSearchResults: []})
    };

    searchTracks = () => {
        spotifyApi.searchTracks(this.state.query).then((data) => {
            this.setState({trackSearchResults: data.tracks.items})
        });
        this.resetDetails()
    };

    getAudioFeatures = (id) => {
        spotifyApi.getAudioFeaturesForTrack(id).then((data) => {
            this.setState({songFeatures: data})
        })
    };

    getAudioAnalasys = (id) => {
        spotifyApi.getAudioAnalysisForTrack(id).then((data) => {
            this.setState({
                songAnalasys: data
            })
        })
    };

    getRecommendations = (params) => {
        spotifyApi.getRecommendations({seed_tracks: this.state.seedTracks.map(track => track.id), ...params}).then((data) => {
            console.log(data.tracks[0]);
            this.setState({
                songRecommendations: data.tracks
            })
        });
        this.clearSearchResults();
    };

    onAutoCompleteChange = (event, {newValue}) => {
        this.setState({
            query: newValue
        });
    };
    clearQuery = () => {
        this.setState({query: ""});
    };
    render() {
        return (
            <div className="App">
                <MetaTags>
                    <title>Find New Music</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1"/>
                </MetaTags>
                <a id="login" href='http://localhost:8000/login'>
                    <button> Login to Spotify</button>
                </a>

                <div className={'form-inline'}>
                    <input autoComplete={"off"} onChange={this.onSearchInputChange} name="track-search" type="text"
                           placeholder="Search tracks"
                           className={'track-search-input'}
                           value={this.state.query}/>
                    <FontAwesomeIcon onClick={this.clearQuery} icon={faTimes} className={"cancel-button"}/>
                    <button onClick={this.searchTracks} className={'btn btn-info name-edit-save-button'}>Search Tracks
                    </button>
                </div>
                <div>
                    {
                        this.state.seedTracks.length > 0 &&
                        <div>

                            <SeedTracksList seedTracks={this.state.seedTracks}
                                            getRecommendations={this.getRecommendations}
                                            removeFromSeedTracks={this.removeFromSeedTracks}/>
                        </div>
                    }
                </div>
                {this.state.trackSearchResults.length > 0 &&
                <SearchResults trackSearchResults={this.state.trackSearchResults}
                               caption="Search Results"
                               getAudioFeatures={this.getAudioFeatures}
                               getRecommendations={this.getRecommendations}
                               addToSeedTracks={this.addToSeedTracks}
                               getAudioAnalasys={this.getAudioAnalasys}/>}

                {
                    this.state.songFeatures &&
                    <SongFeatures songFeatures={this.state.songFeatures}/>
                }
                {this.state.songRecommendations.length > 0 &&
                <SearchResults trackSearchResults={this.state.songRecommendations}
                               caption="Recommendations"
                               getAudioFeatures={this.getAudioFeatures}
                               getRecommendations={this.getRecommendations}
                               getAudioAnalasys={this.getAudioAnalasys}/>
                }
            </div>
        );
    }
}