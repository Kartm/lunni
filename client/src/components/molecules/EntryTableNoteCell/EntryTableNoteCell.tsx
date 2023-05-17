import { Input, Typography } from "antd";
import React, { memo } from "react";
import { Transaction } from "../../../models/merger";

type EntryTableNoteCellProps = {
  defaultNote: Transaction["note"];
  onNoteChange: (note: Transaction["note"]) => void;
};

export const EntryTableNoteCell = memo(
  ({ defaultNote, onNoteChange }: EntryTableNoteCellProps) => (
    <Input
      defaultValue={defaultNote}
      onChange={(e) => onNoteChange(e.target.value)}
      allowClear
    />
  )
);
