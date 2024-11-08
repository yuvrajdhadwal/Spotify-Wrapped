import React from "react";

type ButtonProps = {
    text: string;
    url: string;
}

// button needs to work as both form submitters and links... separate components? extend one class?

/**
 * Returns a React element containing a styled button tag with the given text and
 * which redirects the user to the given URL when clicked
 *
 * @param props.text the text to be displayed on the button
 * @param props.url the url that the user should be directed to when the button is clicked
 */
function Button(props: ButtonProps) {
    const handleClick = () => {
        window.location.href = props.url;
    };
    return (<button onClick={handleClick} className="lowercase text-2xl px-6 py-3 border-2 border-amber-950 rounded-2xl bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg">
        {props.text}
    </button>);
}

export default Button;