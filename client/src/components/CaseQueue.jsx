import { useState } from "react"

const statusConfig = {
  Resolved: {
    badge: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-400",
    icon: "✓",
    iconBg: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-400",
  },
  Flagged: {
    badge: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-400",
    icon: "!",
    iconBg: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-400",
  },
  "Needs Info": {
    badge: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-400",
    icon: "?",
    iconBg: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-400",
  },
  Pending: {
    badge: "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-400",
    icon: "⋯",
    iconBg: "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-400",
  },
}

const TABS = ["All", "Pending", "Resolved", "Flagged", "Needs Info"]

const CaseQueue = ({ cases, onCaseClick, onNewCase, pollingCaseId }) => {
  const [activeTab, setActiveTab] = useState("All")

  const filteredCases =
    activeTab === "All"
      ? cases
      : cases.filter((c) => c.case_status === activeTab)

  const countFor = (tab) =>
    tab === "All"
      ? cases.length
      : cases.filter((c) => c.case_status === tab).length

  if (cases.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <div className="w-14 h-14 rounded-full bg-gray-200 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 flex items-center justify-center">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-gray-500 dark:text-gray-400">
            <rect x="3" y="3" width="18" height="18" rx="3" />
            <path d="M9 12h6M12 9v6" />
          </svg>
        </div>
        <p className="text-base font-medium text-gray-800 dark:text-gray-100">No cases yet</p>
        <p className="text-sm text-gray-500 dark:text-gray-400 text-center max-w-xs">
          Create your first case and let auto-resolve handle it.
        </p>
        <button
          onClick={onNewCase}
          className="mt-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-100 transition-colors"
        >
          + New case
        </button>
      </div>
    )
  }

  return (
    <div>
      {/* Filter tabs */}
      <div className="flex gap-1 border-b border-gray-300 dark:border-gray-700 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2.5 text-sm font-medium rounded-t-md transition-colors ${
              activeTab === tab
                ? "text-gray-900 dark:text-white border-b-2 border-gray-900 dark:border-white -mb-px"
                : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            }`}
          >
            {tab}
            <span
              className={`ml-2 text-xs px-1.5 py-0.5 rounded-full ${
                activeTab === tab
                  ? "bg-gray-900 dark:bg-white text-white dark:text-gray-900"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
              }`}
            >
              {countFor(tab)}
            </span>
          </button>
        ))}
      </div>

      {/* Case list */}
      <div className="flex flex-col gap-3">
        {filteredCases.length === 0 ? (
          <p className="text-sm text-gray-400 dark:text-gray-500 text-center py-12">
            No {activeTab.toLowerCase()} cases.
          </p>
        ) : (
          filteredCases.map((c) => {
            const config = statusConfig[c.case_status] || statusConfig.Pending
            const isPolling = pollingCaseId === c.case_id

            return (
              <div
                key={c.case_id}
                onClick={() => onCaseClick(c)}
                className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-5 py-4 flex items-center gap-4 cursor-pointer hover:border-gray-400 dark:hover:border-gray-500 hover:shadow-sm transition-all"
              >
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0 ${config.iconBg}`}>
                  {isPolling ? <span className="animate-spin">⟳</span> : config.icon}
                </div>

                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {c.case_title}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    Owner: {c.case_owner} · #{c.case_id}
                  </p>
                </div>

                <span className={`text-xs font-medium px-3 py-1 rounded-full flex-shrink-0 ${config.badge}`}>
                  {isPolling ? "Processing..." : c.case_status}
                </span>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}

export default CaseQueue