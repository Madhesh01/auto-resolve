import { useState, useEffect } from "react"
import CaseQueue from "./components/CaseQueue"
import CreateCaseModal from "./components/CreateCaseModal"
import CaseDetailModal from "./components/CaseDetailModal"
import OrdersTable from "./components/OrdersTable"

const SIMULATE_SCENARIOS = [
  {
    title: "Order status check",
    owner: "Madhesh S.",
    description: "Hi, I haven't received any update on my order. Order number 1003. Can you check the status for me?",
  },
  {
    title: "Cancel order request",
    owner: "Madhesh S.",
    description: "I would like to cancel my order please. Order number 1006.",
  },
  {
    title: "Update shipping address",
    owner: "Madhesh S.",
    description: "I need to change my delivery address for order 1008. New address: 42 Linking Road, Bandra West, Mumbai, MH 400050, India.",
  },
  {
    title: "Item arrived damaged",
    owner: "Madhesh S.",
    description: "I received my order 1012 but the item is broken. The packaging was crushed and the product is unusable.",
  },
  {
    title: "Refund request",
    owner: "Madhesh S.",
    description: "I want a full refund for order 1003. Please process it as soon as possible.",
  },
]

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [view, setView] = useState("cases")

  // Form state
  const [caseTitle, setCaseTitle] = useState("")
  const [caseOwner, setCaseOwner] = useState("")
  const [caseDescription, setCaseDescription] = useState("")
  const [simulateIndex, setSimulateIndex] = useState(0)

  // App/UI state
  const [cases, setCases] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [selectedCase, setSelectedCase] = useState(null)

  // Polling state
  const [caseId, setCaseId] = useState(null)

  useEffect(() => {
    fetchCases()
  }, [])

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [darkMode])

  useEffect(() => {
    if (!caseId) return

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/ticket/${caseId}/status`)
        const data = await res.json()

        if (data.status !== "Pending") {
          clearInterval(interval)
          setCaseId(null)
          fetchCases()
        }
      } catch (e) {
        console.error("Polling error:", e)
        clearInterval(interval)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [caseId])

  const fetchCases = async () => {
    try {
      const res = await fetch("/api/tickets")
      const data = await res.json()
      setCases([...data].reverse())
    } catch (e) {
      console.error("Failed to fetch cases:", e)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    const requestBody = {
      case_title: caseTitle,
      case_owner: caseOwner,
      case_description: caseDescription,
      case_status: "Pending",
    }

    try {
      const res = await fetch("/api/ticket", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      })

      if (!res.ok) throw new Error(`HTTP Error: ${res.status}`)

      const data = await res.json()
      setCaseId(data.case_id)
      fetchCases()
      setIsCreateModalOpen(false)
      setCaseTitle("")
      setCaseOwner("")
      setCaseDescription("")
    } catch (e) {
      console.error("Submit error:", e)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSimulate = () => {
    const scenario = SIMULATE_SCENARIOS[simulateIndex % SIMULATE_SCENARIOS.length]
    setCaseTitle(scenario.title)
    setCaseOwner(scenario.owner)
    setCaseDescription(scenario.description)
    setSimulateIndex((i) => i + 1)
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-300">
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-white tracking-tight">
              auto-resolve
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
              Customer support queue
            </p>
          </div>
          <nav className="flex gap-1">
            <button
              onClick={() => setView("cases")}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                view === "cases"
                  ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              }`}
            >
              Cases
            </button>
            <button
              onClick={() => setView("orders")}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                view === "orders"
                  ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              }`}
            >
              Orders
            </button>
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            {darkMode ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="5" />
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
              </svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
              </svg>
            )}
          </button>
          {view === "cases" && (
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-100 transition-colors"
            >
              + New case
            </button>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {view === "cases" ? (
          <CaseQueue
            cases={cases}
            onCaseClick={setSelectedCase}
            onNewCase={() => setIsCreateModalOpen(true)}
            pollingCaseId={caseId}
          />
        ) : (
          <OrdersTable />
        )}
      </main>

      {isCreateModalOpen && (
        <CreateCaseModal
          caseTitle={caseTitle}
          caseOwner={caseOwner}
          caseDescription={caseDescription}
          setCaseTitle={setCaseTitle}
          setCaseOwner={setCaseOwner}
          setCaseDescription={setCaseDescription}
          onSubmit={handleSubmit}
          onSimulate={handleSimulate}
          onClose={() => setIsCreateModalOpen(false)}
          isLoading={isLoading}
          simulateIndex={simulateIndex}
          totalScenarios={SIMULATE_SCENARIOS.length}
        />
      )}

      {selectedCase && (
        <CaseDetailModal
          caseData={selectedCase}
          onClose={() => setSelectedCase(null)}
          pollingCaseId={caseId}
        />
      )}
    </div>
  )
}

export default App
