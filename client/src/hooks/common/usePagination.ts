import { useState } from "react";

export type Pagination = {
  page: number;
  pageSize: number;
};

export const usePagination = () => {
  const [pagination, setPagination] = useState<Pagination>({
    page: 1,
    pageSize: 50,
  });

  return { pagination, setPagination };
};
