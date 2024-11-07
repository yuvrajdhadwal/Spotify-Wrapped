import React from "react";

type Heading1Props = {
    text: string;
}

function Heading1(props: Heading1Props) {

    return (<h1 className="text-6xl text-black lowercase">
        {props.text}
    </h1>);
}

export default Heading1;