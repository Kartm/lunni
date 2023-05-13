import React from "react";
import { Transaction } from "../../../models/merger";

type EntryTableDescriptionCellProps = {
  description: Transaction["description"];
};

export const EntryTableDescriptionCell = ({
  description,
}: EntryTableDescriptionCellProps) => (
  <span title={description}>{description}</span>
);
