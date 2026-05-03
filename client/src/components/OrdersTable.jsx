import { useState, useEffect } from "react"

const statusConfig = {
  PLACED:            "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-400",
  CONFIRMED:         "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-400",
  SHIPPED:           "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-400",
  OUT_FOR_DELIVERY:  "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-400",
  DELIVERED:         "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-400",
  CANCELLED:         "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-400",
  REFUNDED:          "bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-400",
  ESCALATED:         "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300",
  DAMAGED:           "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-400",
}

const OrdersTable = () => {
  const [orders, setOrders] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetch("/api/orders")
      .then((r) => r.json())
      .then((data) => setOrders(data))
      .catch(console.error)
      .finally(() => setIsLoading(false))
  }, [])

  if (isLoading) {
    return (
      <div className="flex justify-center py-24">
        <div className="w-6 h-6 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-sm text-gray-500 dark:text-gray-400">{orders.length} orders</p>
      </div>

      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700">
              <th className="text-left px-5 py-3 text-xs font-medium text-gray-500 dark:text-gray-400">Order</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-gray-500 dark:text-gray-400">Status</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 hidden md:table-cell">Address</th>
              <th className="text-right px-5 py-3 text-xs font-medium text-gray-500 dark:text-gray-400">Price</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order, i) => (
              <tr
                key={order.order_no}
                className={`border-b border-gray-100 dark:border-gray-800 last:border-0 ${
                  i % 2 === 0 ? "" : "bg-gray-50/50 dark:bg-gray-800/20"
                }`}
              >
                <td className="px-5 py-3 font-medium text-gray-900 dark:text-gray-100">
                  #{order.order_no}
                </td>
                <td className="px-5 py-3">
                  <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${statusConfig[order.status] || "bg-gray-100 text-gray-700"}`}>
                    {order.status}
                  </span>
                </td>
                <td className="px-5 py-3 text-gray-500 dark:text-gray-400 hidden md:table-cell max-w-xs truncate">
                  {order.address}
                </td>
                <td className="px-5 py-3 text-right font-medium text-gray-900 dark:text-gray-100">
                  ₹{order.price.toLocaleString("en-IN")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default OrdersTable
