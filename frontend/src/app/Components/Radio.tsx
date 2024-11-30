import React from "react";

type RadioProps = {
    name: string;
    value: string;
    text: string;
    onChange?: () => void;
    checked?: boolean;
};

/**
 * Returns a React element containing a radio button associated with a value and labeled with the given text
 *
 * @param props.text the text to be displayed in the radio button's label
 * @param props.name the name of the data that the button should send, e.g. time_range
 * @param props.value the value that the radio button shou be associated with, e.g. 1 year
 * @param props.onChange change of value
 * @param props.checked if the radio button is checked on
 */
const Radio: React.FC<RadioProps> = ({ name, value, text, onChange, checked }) => (
    <label>
        <input type="radio" name={name} value={value} onChange={onChange} checked={checked} className={"mr-2 w-5 h-5"} />
        {text}
    </label>
);

export default Radio;