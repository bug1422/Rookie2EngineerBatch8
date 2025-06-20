import { cn } from "@/utils/cn";

interface PaginationProps {
  isLoading: boolean;
  /** Current active page number
   * @minimum 1
   */
  currentPage: number;

  /** Maximum number of pages
   * @minimum 1
   */
  maxPage?: number;
  /** Number of pages to show on each side of current page
   * @description Controls how many page numbers are shown on each side of the current page.
   * Total pages shown will be (2 * pageOffset + 1).
   * @example
   * pageOffset={1} // Shows 3 pages total: [prev] 1 2 3 [next]
   * pageOffset={2} // Shows 5 pages total: [prev] 1 2 3 4 5 [next]
   * @default 1
   * @minimum 1
   */
  pageOffset?: number;
  /** Callback fired when page changes
   * @param value - The new page number
   */
  onChange?: (value: number) => void;
}

const calculatePageRange = (
  currentPage: number,
  maxPage: number,
  pageOffset: number,
  pageToShow: number
) => {
  if (maxPage <= pageToShow) {
    return Array.from({ length: maxPage }, (_, i) => i + 1);
  }
  if (currentPage <= pageOffset + 1) {
    return Array.from({ length: pageToShow }, (_, i) => i + 1);
  }
  if (currentPage >= maxPage - pageOffset) {
    return Array.from(
      { length: pageToShow },
      (_, i) => maxPage - pageToShow + i + 1
    );
  }
  return Array.from(
    { length: pageToShow },
    (_, i) => currentPage - pageOffset + i
  );
};
export default function Pagination({
  isLoading = false,
  currentPage,
  maxPage = 0,
  pageOffset = 1,
  onChange,
}: PaginationProps) {
  const pageToShow = pageOffset * 2 + 1;
  const pageRange = isLoading
    ? calculatePageRange(
        currentPage,
        currentPage + pageOffset,
        pageOffset,
        pageToShow
      )
    : calculatePageRange(currentPage, maxPage, pageOffset, pageToShow);
  const setValue = (newValue: number) => {
    console.log("setting");
    if (newValue != currentPage && newValue >= 1 && newValue <= maxPage) {
      onChange?.(newValue);
    }
  };
  const handlePrevValue = () => {
    setValue(currentPage - 1);
  };
  const handleNextValue = () => {
    setValue(currentPage + 1);
  };
  const handleDefinedValue = (newValue: number) => {
    setValue(newValue);
  };
  return (
    <div className="relative flex justify-center sm:justify-end">
      <div className="bottom-12 sm:block flex items-center">
        <div
          className={cn(
            "btn rounded-none border-neutral-content rounded-l-md",
            !isLoading && currentPage > 1
              ? "text-primary "
              : "text-neutral-content"
          )}
          onClick={() => {
            if (!isLoading) handlePrevValue();
          }}
        >
          Previous
        </div>
        {pageRange.map((pageNumber) => (
          <div
            key={"pagination-" + pageNumber}
            className={cn(
              "w-12 btn rounded-none",
              !isLoading && currentPage == pageNumber
                ? "btn-primary"
                : "text-primary"
            )}
            onClick={() => {
              if (!isLoading && currentPage != pageNumber)
                handleDefinedValue(pageNumber);
            }}
          >
            {isLoading ? " " : pageNumber}
          </div>
        ))}
        <div
          className={cn(
            "btn rounded-none border-neutral-content rounded-r-md",
            !isLoading && currentPage < maxPage
              ? "text-primary "
              : "text-neutral-content"
          )}
          onClick={() => {
            if (!isLoading) handleNextValue();
          }}
        >
          Next
        </div>
      </div>
    </div>
  );
}
