import asyncio, httpx, time

TICKETS = [
    {"case_title": "Where is my order", "case_owner": "Alice", "case_description": "I placed order #1001 last week and haven't received any updates. Can you check the status?", "case_status": "Pending"},
    {"case_title": "Cancel my order", "case_owner": "Bob", "case_description": "Please cancel order #1002 immediately, I changed my mind.", "case_status": "Pending"},
    {"case_title": "Wrong shipping address", "case_owner": "Carol", "case_description": "I entered the wrong address for order #1003. Please update it to 45 Oak Street, Mumbai.", "case_status": "Pending"},
    {"case_title": "Cancel order request", "case_owner": "Dave", "case_description": "I want to cancel order #1004, item is no longer needed.", "case_status": "Pending"},
    {"case_title": "No order number provided", "case_owner": "Eve", "case_description": "My package hasn't arrived yet, please help.", "case_status": "Pending"},
]

async def submit_ticket(client: httpx.AsyncClient, i: int) -> int | None:
    ticket = TICKETS[i % len(TICKETS)]
    try:
        res = await client.post("http://localhost:8000/ticket", json=ticket, timeout=10)
        case_id = res.json().get("case_id")
        print(f"[{i+1:02}] submitted → case_id: {case_id}")
        return case_id
    except Exception as e:
        print(f"[{i+1:02}] failed → {e}")
        return None

async def wait_for_resolution(client: httpx.AsyncClient, case_id: int, start: float):
    while True:
        await asyncio.sleep(3)
        try:
            res = await client.get(f"http://localhost:8000/ticket/{case_id}/status", timeout=5)
            status = res.json().get("status")
            if status != "Pending":
                elapsed = time.time() - start
                print(f"  case_id {case_id} → {status} in {elapsed:.1f}s")
                return elapsed
        except Exception as e:
            print(f"  case_id {case_id} polling error → {e}")

async def main():
    N = 20
    async with httpx.AsyncClient() as client:

        # Phase 1: submit all tickets
        ingest_start = time.time()
        tasks = [submit_ticket(client, i) for i in range(N)]
        case_ids = await asyncio.gather(*tasks)
        ingest_elapsed = time.time() - ingest_start
        print(f"\n{N} tickets submitted in {ingest_elapsed:.2f}s")
        print(f"Ingestion throughput: {N/ingest_elapsed:.1f} tickets/sec")

        # Phase 2: poll until all resolved
        print(f"\nWaiting for worker to resolve all tickets...\n")
        resolution_start = time.time()
        valid_ids = [cid for cid in case_ids if cid]
        latencies = await asyncio.gather(*[wait_for_resolution(client, cid, resolution_start) for cid in valid_ids])

        print(f"\n--- Results ---")
        print(f"Avg resolution latency : {sum(latencies)/len(latencies):.1f}s")
        print(f"Min                    : {min(latencies):.1f}s")
        print(f"Max                    : {max(latencies):.1f}s")
        print(f"Total wall time        : {time.time()-resolution_start:.1f}s")

if __name__ == "__main__":
    asyncio.run(main())