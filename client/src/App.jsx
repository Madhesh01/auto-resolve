import { useState, useEffect } from "react"
import CaseQueue from "./components/CaseQueue"
import CreateCaseModal from "./components/CreateCaseModal"
import CaseDetailModal from "./components/CaseDetailModal"

function App() {
  const [darkMode, setDarkMode] = useState(false)

  // Form state
  const [caseTitle, setCaseTitle] = useState("")
  const [caseOwner, setCaseOwner] = useState("")
  const [caseDescription, setCaseDescription] = useState("")

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
        const res = await fetch(`http://localhost:8000/ticket/${caseId}/status`)
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
      const res = await fetch("http://localhost:8000/tickets")
      const data = await res.json()
      setCases(data)
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
      const res = await fetch("http://localhost:8000/ticket", {
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
    setCaseTitle("Order not received — John D.")
    setCaseOwner("Sarah Kim")
    setCaseDescription(
      "Customer placed order #4821 on Mar 18 but has not received it. Requesting status update or refund."
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-300">
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-gray-900 dark:text-white tracking-tight">
            auto-resolve
          </h1>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            Customer support queue
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-100 transition-colors"
          >
            + New case
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <CaseQueue
          cases={cases}
          onCaseClick={setSelectedCase}
          onNewCase={() => setIsCreateModalOpen(true)}
          pollingCaseId={caseId}
        />
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