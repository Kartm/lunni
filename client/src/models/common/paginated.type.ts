export type Paginated<T> = {
    count: number;
    total_pages: number;
    results: Array<T>;
};
