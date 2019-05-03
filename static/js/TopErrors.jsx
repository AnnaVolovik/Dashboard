import React from "react";

function drawErrors(props) {

    let backgroundColors = ['#FFCC00', '#5856D5', '#2196F3', '#A0B0B9'];

    return props.map((error, index) =>
            <div key={index} className="square" style={{width: error.width, backgroundColor: backgroundColors[index]}}></div>);
}

function listErrors(props) {

    let colors = ['yellow', 'violet', 'blue', 'grey-background'];

    return props.map((error, index) =>
            <div className="wrapper" key={index}>
                <div className="circle_wrapper">
                    <div className={`square_rounded ${colors[index]}`}></div>
                </div>
                <div className="text_wrapper"><p>{error.code}: {error.count}</p></div>
            </div>);

}

export default function TopErrors (props) {

        return (<div className="topErrors">{drawErrors(props.errors)}{listErrors(props.errors)}</div>);
}

