import React, {Component} from 'react';
import RangeInput from "../RangeInput/RangeInput";
import "./SeedTrackList.css"

export default class SearchResults extends Component {
    constructor() {
        super();
        this.state = {
            showParams: false,
            params: {
                max_popularity: 100,
                max_acousticness: 1,
                max_danceability: 1,
                max_energy: 1,
                max_instrumentalness: 1,
                max_speechiness: 1,
                max_tempo: 208,
                max_valence: 1,
                min_popularity: 0,
                min_acousticness: 0,
                min_danceability: 0,
                min_energy: 0,
                min_instrumentalness: 0,
                min_speechiness: 0,
                min_tempo: 24,
                min_valence: 0,
            }
        }
    };

    updateRangeInput = (type, min, max) => {
        let retObj = {...this.state.params};
        retObj[`min_${type}`] = min;
        retObj[`max_${type}`] = max;
        this.setState(retObj);
    };
    toggleShowParams = () => {
        this.setState({showParams: !this.state.showParams});
    };

    render() {
        return (
            <div className="App">
                <button onClick={() => this.props.getRecommendations(this.state)}>Get Recommendations</button>
                <table>
                    <caption>Seed Tracks</caption>
                    <tbody>
                    {
                        this.props.seedTracks.length > 0 &&
                        this.props.seedTracks.map((track, i) => {
                            return <tr key={i}>
                                <td> {track.name}</td>
                                <td> {track.artists.map((artist) => artist.name).join(', ')}</td>
                                <td>
                                    <button onClick={() => this.props.getAudioFeatures(track.id)}>Get Audio Features
                                    </button>
                                </td>
                                <td>
                                    <button onClick={() => this.props.removeFromSeedTracks(track)}>Remove
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
                <button onClick={this.toggleShowParams}>{this.state.showParams? "Hide Params": "Show Params"}</button>
                { this.state.showParams &&
                    <div className={"param-container"}>
                        <RangeInput label={'Popularity'}
                                    min={0}
                                    minLabel={'Not Popular'}
                                    maxLabel={'Popular'}
                                    initMin={0}
                                    initMax={100}
                                    onChange={(min, max) => {
                                        this.updateRangeInput(
                                            'energy',
                                            min,
                                            max
                                        );
                                    }}
                                    step={1}
                                    max={100}/>
                        <RangeInput
                            label='Energy'
                            minLabel='Chill'
                            maxLabel='No chill'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'energy',
                                    min,
                                    max
                                );
                            }}
                        />
                        <RangeInput
                            label='Speechiness'
                            minLabel='No Speechiness'
                            maxLabel='All Speechiness'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'speechiness',
                                    min,
                                    max
                                );
                            }}
                        />
                        <RangeInput
                            label='Instrumentalness'
                            minLabel='Not Instrumental'
                            maxLabel='Completely Instrumental'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'instrumentalness',
                                    1 - max,
                                    1 - min
                                );
                            }}
                        />
                        <RangeInput
                            label='Tempo'
                            minLabel='Slow'
                            maxLabel='Fast'
                            initMin={24}
                            initMax={208}
                            min={24}
                            max={208}
                            step={2}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'tempo',
                                    min,
                                    max
                                );
                            }}
                        />
                        <RangeInput
                            label='Dancable'
                            minLabel='Not at all'
                            maxLabel='Involuntary ass shaking'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'danceability',
                                    min,
                                    max
                                );
                            }}
                        />
                        <RangeInput
                            label='Mood'
                            minLabel='Negative'
                            maxLabel='Positive'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'valence',
                                    min,
                                    max
                                );
                            }}
                        />
                        <RangeInput
                            label='Acoustics'
                            minLabel='All electronic'
                            maxLabel='All acoustic'
                            initMin={0}
                            initMax={1}
                            min={0}
                            max={1}
                            step={0.02}
                            onChange={(min, max) => {
                                this.updateRangeInput(
                                    'acousticness',
                                    min,
                                    max
                                );
                            }}
                        />
                    </div>
                }
            </div>
        );
    }
}