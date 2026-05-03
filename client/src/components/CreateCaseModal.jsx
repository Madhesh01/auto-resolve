const CreateCaseModal = ({
  caseTitle,
  caseOwner,
  caseDescription,
  setCaseTitle,
  setCaseOwner,
  setCaseDescription,
  onSubmit,
  onSimulate,
  onClose,
  isLoading,
  simulateIndex,
  totalScenarios,
}) => {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-base font-semibold text-gray-900 dark:text-white">New case</h2>
          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center rounded-md text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <form onSubmit={onSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-600 dark:text-gray-400">Case title</label>
            <input
              type="text"
              placeholder="e.g. Order status check"
              value={caseTitle}
              onChange={(e) => setCaseTitle(e.target.value)}
              required
              className="border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white focus:border-transparent"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-600 dark:text-gray-400">Case owner</label>
            <input
              type="text"
              placeholder="e.g. Madhesh S."
              value={caseOwner}
              onChange={(e) => setCaseOwner(e.target.value)}
              required
              className="border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white focus:border-transparent"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-600 dark:text-gray-400">Description</label>
            <textarea
              placeholder="Describe the issue in detail..."
              value={caseDescription}
              onChange={(e) => setCaseDescription(e.target.value)}
              required
              rows={4}
              className="border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white focus:border-transparent resize-none"
            />
          </div>

          <div className="flex gap-3 mt-2">
            <button
              type="button"
              onClick={onSimulate}
              className="flex-1 flex items-center justify-center gap-2 border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-sm font-medium py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="17 1 21 5 17 9" />
                <path d="M3 11V9a4 4 0 0 1 4-4h14" />
                <polyline points="7 23 3 19 7 15" />
                <path d="M21 13v2a4 4 0 0 1-4 4H3" />
              </svg>
              Simulate
              <span className="text-xs text-gray-400 dark:text-gray-500">
                {(simulateIndex % totalScenarios) + 1}/{totalScenarios}
              </span>
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium py-2.5 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Submitting..." : "Submit case"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateCaseModal
