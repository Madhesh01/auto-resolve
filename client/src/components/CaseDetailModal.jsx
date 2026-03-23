const statusConfig = {
  Resolved: {
    badge: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-400",
    box: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800",
    label: "text-green-800 dark:text-green-300",
  },
  Flagged: {
    badge: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-400",
    box: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800",
    label: "text-red-800 dark:text-red-300",
  },
  "Needs Info": {
    badge: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-400",
    box: "bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800",
    label: "text-amber-800 dark:text-amber-300",
  },
  Pending: {
    badge: "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-400",
    box: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800",
    label: "text-blue-800 dark:text-blue-300",
  },
}

const CaseDetailModal = ({ caseData, onClose, pollingCaseId }) => {
  const config = statusConfig[caseData.case_status] || statusConfig.Pending
  const isPolling = pollingCaseId === caseData.case_id

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl w-full max-w-lg p-6">
        <div className="flex items-start justify-between mb-5">
          <div>
            <h2 className="text-base font-semibold text-gray-900 dark:text-white">
              {caseData.case_title}
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">#{caseData.case_id}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none ml-4 flex-shrink-0"
          >
            ×
          </button>
        </div>

        <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden mb-4">
          <div className="flex justify-between items-center px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <span className="text-xs text-gray-500 dark:text-gray-400">Owner</span>
            <span className="text-sm font-medium text-gray-800 dark:text-gray-200">{caseData.case_owner}</span>
          </div>
          <div className="flex justify-between items-center px-4 py-3">
            <span className="text-xs text-gray-500 dark:text-gray-400">Status</span>
            <span className={`text-xs font-medium px-3 py-1 rounded-full ${config.badge}`}>
              {isPolling ? "Processing..." : caseData.case_status}
            </span>
          </div>
        </div>

        <div className="mb-4">
          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">Description</p>
          <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
            {caseData.case_description}
          </p>
        </div>

        <div>
          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5 uppercase tracking-wide">
            AI resolution
          </p>
          {isPolling ? (
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl px-4 py-4">
              <p className="text-sm text-blue-700 dark:text-blue-400 flex items-center gap-2">
                <span className="animate-spin">⟳</span>
                Auto-resolve is working on this case...
              </p>
            </div>
          ) : caseData.ai_resolution ? (
            <div className={`border rounded-xl px-4 py-4 ${config.box}`}>
              <p className={`text-sm leading-relaxed ${config.label}`}>
                {caseData.ai_resolution}
              </p>
            </div>
          ) : (
            <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-4">
              <p className="text-sm text-gray-400 dark:text-gray-500">No resolution yet.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CaseDetailModal