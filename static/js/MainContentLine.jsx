import React from "react";
import SVGElement from './SVGElement';


function LeftSide(props) {
    return (
            <div className="LeftSide">
                {<SVGElement keyword={props.keyword} color={props.color}/>}
                <div className="text_wrapper">
                    <h2>{props.keyword.charAt(0).toUpperCase() + props.keyword.slice(1)}</h2>
                    <div className={`emphasized ${props.color}`}><span>{props.content.diff}%</span></div>
                    <p><br />{props.content.current} {props.day}</p>
                    <p className="grey"><br />{props.content.previous} Last Friday</p>
                </div>
            </div>
        );
}

function RightSide (props) {

    const helpItems = {
        searches: ["Searches", "Pessimisation"],
        clicks: ["CTR", "Clicks"],
        bookings: ["STR", "Bookings", "Avg. Check"]
    };
    const descriptions = {
        searches: "You get " + props.param1 + props.param2 +"% traffic on mobile and desktop devices.",
        clicks: 'Conversion from searches to clicks on all devices.',
        bookings: 'Conversion from clicks to bookings on all devices.',
    };

    const headings = {
        searches: ["Mobile traffic: " + props.param1 + "%", "Web traffic: "+ props.param2 +"%"],
        clicks: ["CTR: "+ props.param1 + "%"],
        bookings: ["STR: " + props.param1+"%", "Avg. Check: " + props.param2]
    };

    const helpLinks = helpItems[props.keyword].map((helpItem, index) =>
        <a key={index} href="#">{helpItem}</a>).reduce((prev, curr) => [prev, ', ', curr]);

    const headingsSorted = headings[props.keyword].map((heading, index) =>
        <h2 key={index}>{heading}</h2>).reduce((prev, curr, index) => [prev, <br key={index+4}/>, curr]);

    return (
        <div className="RightSide">
          <div className="text_wrapper">
            {headingsSorted}
            <p className="grey"><br />{descriptions[props.keyword]}</p>
            <p><br />Help: {helpLinks} </p>
          </div>
        </div>
    );
}

export default function MainContentLine (props) {
    return (
            <div className='mainContentLine'>
                {<LeftSide keyword={props.keyword} content={props.content} color={props.color}/>}
                {<RightSide keyword={props.keyword}
                            param1={props.content.param1}
                            param2={props.content.param2}
                />}
            </div>
        );

}
