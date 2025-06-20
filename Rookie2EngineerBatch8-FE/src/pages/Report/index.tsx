import PageLayout from "@/components/layouts/PageLayout";
import Pagination from "@/components/UI/Pagination";
import { ReportTable } from "@/components/UI/Table/ReportTable";
import { useReportData } from "@/hooks/useReportData";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { reportService } from "@/api/reportService";
import toast from "@/components/UI/Toast";
import { useCallback, useRef } from "react";
import { AxiosError } from "axios";

const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

export default function Report() {
  useBreadcrumbs([{ label: "Report" }]);
  const downloadRef = useRef<HTMLAnchorElement>(null);
  const {
    reports,
    isLoading,
    paginationMeta,
    currentPage,
    sortBy,
    sortDirection,
    handleSort,
    handlePageChange,
  } = useReportData();

  const handleExport = useCallback(async () => {
    if (downloadRef.current !== null) {
      try {
        const response = await reportService.download_report();
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });
        const url = window.URL.createObjectURL(blob);

        let filename = "report.xlsx";
        const disposition = response.headers["content-disposition"];
        if (disposition) {
          const match = disposition.match(/filename="?([^"]+)"?/);
          if (match && match[1]) {
            filename = match[1].trim();
          }
        }
        const link = downloadRef.current;
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
        toast({ duration: 3000, content: "File exported" });
      } catch (error) {
        if (error instanceof AxiosError) {
          toast({
            alertType: "alert-error",
            duration: 3000,
            content: error.message,
          });
        }
      }
    }
  }, [downloadRef]);

  return (
    <PageLayout title="Report">
      <div className="flex flex-col gap-2">
        <div className="flex flex-row justify-end">
          <button
            className="btn btn-primary"
            onClick={handleExport}
            disabled={isLoading || !reports.length}
          >
            Export
          </button>
        </div>

        <ReportTable
          reports={reports}
          isLoading={isLoading}
          pageSize={PAGE_SIZE}
          sortBy={sortBy}
          sortDirection={sortDirection}
          onSort={handleSort}
        />

        <div className="flex justify-end items-center w-full mb-4">
          <Pagination
            isLoading={isLoading}
            currentPage={currentPage}
            maxPage={paginationMeta?.total_pages || 0}
            onChange={handlePageChange}
          />
        </div>
        <a ref={downloadRef} id="download-link" className="hidden" />
      </div>
    </PageLayout>
  );
}
