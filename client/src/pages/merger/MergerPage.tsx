import {EntryTable} from "../../components/EntryTable";
import React from "react";
import {FileUpload} from "../../components/FileUpload/FileUpload";
import {useUploadFile} from "../../hooks/merger/useUploadFile";

export const MergerPage = () => {
    const {isLoading, mutate} = useUploadFile();

    return <div>

        <FileUpload isUploading={isLoading} onFileUpload={fileUpload => mutate(fileUpload)}/>
        <EntryTable/>
    </div>

}