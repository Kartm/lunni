import {EntryTable} from "../../components/EntryTable";
import React, {useState} from "react";
import {FileUpload} from "../../components/FileUpload/FileUpload";
import {useUploadFile} from "../../hooks/merger/useUploadFile";
import {useGetTransactions} from "../../hooks/merger/useGetTransactions";
import {MergeButton} from "../../components/MergeButton";
import {Key} from "antd/es/table/interface";
import {useMergeMutations} from "../../hooks/merger/useMergeTransactions";

export const MergerPage = () => {
    const {isLoading, mutate} = useUploadFile();
    const {data} = useGetTransactions();
    const [mergeSelection, setMergeSelection] = useState<Key[]>([])
    const mergeTransactions = useMergeMutations();

    const handleMerge = (sourceId: number, targetId: number, amount: number) => {
        mergeTransactions.mutate({
            from_transaction: sourceId,
            to_transaction: targetId,
            amount: amount * 1
        })
    }

    return <div>
        <FileUpload isUploading={isLoading} onFileUpload={fileUpload => mutate(fileUpload)}/>
        <MergeButton mergeSelection={mergeSelection} data={data?.transactions || []} onMerge={handleMerge}/>
        <EntryTable isLoading={isLoading} data={data?.transactions || []} onMergeSelectionChange={setMergeSelection}/>
    </div>

}