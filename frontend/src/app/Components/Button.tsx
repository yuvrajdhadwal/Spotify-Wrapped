import React from "react";

type ButtonProps = {
    text: string;
    url: string;
}

// button needs to work as both form submitters and links... separate components? extend one class?

function Button(props: ButtonProps) {
    const handleClick = () => {
        window.location.href = props.url;
    };
    return (<button onClick={handleClick} className="lowercase text-2xl px-6 py-3 border-2 border-amber-950 rounded-2xl bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg">
        {props.text}
    </button>);
}

export default Button;