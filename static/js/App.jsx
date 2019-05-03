import React from "react";
import NavBar from "./NavBar";
import TopStats from './TopStats';
import TopErrors from './TopErrors';
import MainContent from './MainContent';

require('../css/styles.css');

var $ = require('jquery');
require('jquery-ui-bundle');

export default class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            activeId: 2,
            activeClasses: [{name: "Last hour", isActive: false},
                            {name: "Today", isActive: false},
                            {name:"Yesterday", isActive: false},
                            {name: "Last 3 hours", isActive: true}]
        };
        this.getPythonData = this.getPythonData.bind(this);
    }

    getPythonData(index) {
        // get stats data from the backend & set active nav button
        let indexRef = {0: "last_hour", 1: "today", 2: "yesterday", 3: "last_3days"};
        $.getJSON(window.location.href + 'get_data?keyword='+ indexRef[index], (data) => {
            this.setState({
                data: data,
                activeId: index})
            });
    }

    componentDidMount() {
        this.getPythonData(2);
    }

    render() {

        return (
                <div className='contents'>
                    <h1>Main metrics</h1>
                    <NavBar activeClasses={this.state.activeClasses}
                            activeId={this.state.activeId}
                            onClick={this.getPythonData} />
                    {this.state.data ? <TopStats content={this.state.data.top_statistics}/> : null}
                    {this.state.data ? <TopErrors errors={this.state.data.top_errors}/> : null}
                    {this.state.data ? <MainContent content={this.state.data.content} /> : null}
                </div>
        );
    }
}