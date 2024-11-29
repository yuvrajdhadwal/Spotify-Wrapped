import React from "react";

type InputProps = {
    label: string;
    name: string;
    value: string;
    type: string;
    onChange?: (...args: any[]) => any;
}

/**
 * Returns a React element containing a div which has a typing input field and an associated label.
 *
 * @param props.label the label text
 * @param props.name the name associated with the input
 * @param props.value the value associated with the name
 * @param props.type the type of the input (type, password)
 * @param props.onChange the function to be called when the input is changed. optional
 */
function Input(props: InputProps) {
    return (
        <div className={"mb-2 justify-end items-end"}>
            <label className={"mr-2 w-64 inline-block text-right"}>{props.label}</label>
            <input type={props.type} name={props.name} value={props.value} onChange={props.onChange} className={"border-2 mr-40"}/>
        </div>
    );
}

export default Input;