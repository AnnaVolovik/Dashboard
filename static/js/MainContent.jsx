import React from "react";
import MainContentLine from "./MainContentLine";

export default function MainContent (props) {

    let keys = Object.keys(props.content);
    let content = [];
    for (let i=0; i<keys.length; i++) {
        let color = i % 2 === 0 ? "green" : "red-background";
        let keyword = keys[i];
        content.push(<MainContentLine key={keyword} content={props.content[keyword]} keyword={keyword} color={color}/>)
    }
    return (<div>{content.reduce((prev, curr, index) => [prev, <hr key={index}/>, curr])}</div>)

}
