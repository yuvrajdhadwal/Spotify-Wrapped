import React from "react";
import BodyText from "@/app/Components/BodyText";

type RadioProps = {
    name: string;
    value: string;
    text: string;
}

/**
 * Returns a React element containing a radio button associated with a value and labeled with the given text
 *
 * @param props.text the text to be displayed in the radio button's label
 * @param props.name the name of the data that the button should send, e.g. time_range
 * @param props.value the value that the radio button shou be associated with, e.g. 1 year
 */
function Radio(props: RadioProps) {
    return (
        <label className="flex items-center pl-6">
            <input type="radio" name={props.name} value={props.value}></input>
            <BodyText text={props.text}/>
        </label>
    );
}

export default Radio;