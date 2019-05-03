import React from "react";

export default class NavBar extends React.Component {

    render () {
        return (<nav>
                    {this.props.activeClasses.map((el, index) =>
                        <button key={'button_'+index} onClick={() => this.props.onClick(index)}
                        className={index === this.props.activeId ? "active" : "inactive"}>{el.name}</button>)}
                </nav>)
    }
}