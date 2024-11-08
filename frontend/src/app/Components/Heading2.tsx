import React from "react";

type Heading2Props = {
    text: string;
}

/**
 * Returns a React element containing a styled h2 tag with the given text
 *
 * @param props.text the text to be displayed in the h2 tag
 */
function Heading2(props: Heading2Props) {

    return (<h2 className="text-5xl text-black lowercase">
        {props.text}
    </h2>);
}

export default Heading2;