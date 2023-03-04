import {EntryTable} from "../../components/EntryTable";
import React, {useState} from "react";
import {FileUpload} from "../../components/FileUpload/FileUpload";
import {useUploadFile} from "../../hooks/merger/useUploadFile";
import {useGetTransactions} from "../../hooks/merger/useGetTransactions";
import {MergeButton} from "../../components/MergeButton";
import {Key} from "antd/es/table/interface";

export const MergerPage = () => {
    const {isLoading, mutate} = useUploadFile();
    const {data} = useGetTransactions();
    const [mergeSelection, setMergeSelection] = useState<Key[]>([])

    return <div>
        <FileUpload isUploading={isLoading} onFileUpload={fileUpload => mutate(fileUpload)}/>
        <MergeButton mergeSelection={mergeSelection}/>
        <EntryTable isLoading={isLoading} data={data?.transactions || []} onMergeSelectionChange={setMergeSelection}/>
    </div>

}