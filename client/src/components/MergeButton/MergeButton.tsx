import {Button} from "antd";
import {Key} from "antd/es/table/interface";

type MergeButtonProps = {
    mergeSelection: Key[];
}

export const MergeButton = ({mergeSelection}: MergeButtonProps) => {
    return <Button disabled={mergeSelection.length !== 2}>Merge</Button>
}