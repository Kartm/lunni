import {EntryTable} from "../../components/EntryTable";
import React from "react";
import {FileUpload} from "../../components/FileUpload/FileUpload";
import {useUploadFile} from "../../hooks/merger/useUploadFile";
import {useGetTransactions} from "../../hooks/merger/useGetTransactions";

export const MergerPage = () => {
    const {isLoading, mutate} = useUploadFile();
    const {data} = useGetTransactions();

    return <div>

        <FileUpload isUploading={isLoading} onFileUpload={fileUpload => mutate(fileUpload)}/>
        <EntryTable data={data?.transactions || []}/>
    </div>

}