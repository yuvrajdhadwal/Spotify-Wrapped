import React from "react";

type Heading2Props = {
    text: string;
}

function Heading2(props: Heading2Props) {

    return (<h2 className="text-5xl text-black lowercase">
        {props.text}
    </h2>);
}

export default Heading2;