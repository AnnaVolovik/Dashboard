import React from "react";

function TopStatsElement(props) {
    return (
            <div className="TopStatsElement">
                <div className="circle_wrapper"><div className="circle green"></div></div>
                <div className="text_wrapper">
                    <h2>{props.content.name}: {props.content.value}%</h2>
                    <p className="grey"><br />Average: {props.content.average}%</p>
                </div>
            </div>
    );
}

export default function TopStats(props) {

    let keys = Object.keys(props.content);
    let content = [];

    for (let i=0; i<keys.length; i++) {
        content.push(<TopStatsElement key={i} content={props.content[keys[i]]}/>)
    }

    return content
}

