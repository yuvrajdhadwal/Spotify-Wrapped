import React from "react";

type ButtonProps = {
    text: string;
    url?: string;
    method?: (...args: any[]) => any;
    extraClasses?: string;
    faded?: boolean;
    small?: boolean;
}

/**
 * Returns a React element containing a styled button tag with the given text and
 * which redirects the user to the given URL when clicked
 *
 * @param props.text the text to be displayed on the button
 * @param props.url the url that the user should be directed to when the button is clicked. optional
 * @param props.method the function that executes on button click. optional (redirect to url by default)
 * @param props.extraClasses any other extra styling classes. optional
 */
function Button(props: ButtonProps) {
    const handleClick = () => {
        window.location.href = props.url ? props.url : "";
    };
    const color = props.faded ? " bg-gradient-to-tr from-red-400 to-yellow-200 border-amber-700": " bg-gradient-to-tr from-red-500 to-yellow-500 border-amber-950";
    const size = props.small ? " text-xl px-4 py-2": " text-2xl px-6 py-3";
    const clickMethod = props.method ? props.method : handleClick;
    const classes = props.extraClasses + color + size + " lowercase border-2 rounded-2xl text-white shadow-lg";
    return (<button onClick={clickMethod} className={classes}>
        {props.text}
    </button>);
}

export default Button;