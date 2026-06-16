import schedule
import time
from fetcher import main

def start():
    print("Scheduler started. Refreshing every 3 hours...")
    # Run immediately on startup
    main()
    # Repeat every 3 hours
    schedule.every(3).hours.do(main)
    while True:
        # Check if a job is due
        schedule.run_pending()
        # Wait 60 seconds before checking again
        time.sleep(60)