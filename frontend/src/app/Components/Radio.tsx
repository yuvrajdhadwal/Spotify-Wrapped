            Radio

import React from "react";

type RadioProps = {
    name: string;
    value: string;
    text: string;
}

function Radio(props: RadioProps) {
    return (
        <label className="pl-6">
            <input type="radio" name={props.name} value={props.value}></input>{props.text}
        </label>
    );
}

export default Radio;