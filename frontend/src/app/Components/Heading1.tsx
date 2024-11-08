import React from "react";

type Heading1Props = {
    text: string;
}

/**
 * Returns a React element containing a styled h1 tag with the given text
 *
 * @param props.text the text to be displayed in the h1 tag
 */
function Heading1(props: Heading1Props) {

    return (<h1 className="text-6xl text-black lowercase">
        {props.text}
    </h1>);
}

export default Heading1;