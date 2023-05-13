import { Input, Typography } from "antd";
import React from "react";
import { Transaction } from "../../../models/merger";

const { Text } = Typography;

type EntryTableNoteCellProps = {
  defaultNote: Transaction["note"];
  onNoteChange: (note: Transaction["note"]) => void;
};

export const EntryTableNoteCell = ({
  defaultNote,
  onNoteChange,
}: EntryTableNoteCellProps) => (
  <Input
    defaultValue={defaultNote}
    onChange={(e) => onNoteChange(e.target.value)}
    allowClear
  />
);
