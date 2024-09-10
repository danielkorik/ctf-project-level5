from env import ENV, ENDPOINT_URL, logger
import asyncio
import aiohttp

# Define the batch size and initialize the flag event
batch_size = 1000
flag_found = asyncio.Event()

# Asynchronous function to fetch a batch of data from the endpoint
async def fetch_batch(session, start, end):
    # If the flag has already been found, stop further fetching
    if flag_found.is_set():
        return []

    # Set the parameters for batch fetching
    params = {
        'start': start,
        'end': end
    }

    try:
        # Make an asynchronous GET request with the parameters
        async with session.get(ENDPOINT_URL, params=params) as response:
            # Check if the response is successful
            if response.status == 200:
                data = await response.json()
                logger.info(f"Fetched batch from {start} to {end}")

                # Check if a flag is present in the fetched data
                for entry in data:
                    if 'flag' in entry:
                        logger.critical(f"Found flag: {entry['flag']}")
                        flag_found.set()  # Signal that the flag was found
                        return data

                return data
            else:
                logger.error(f"Failed to fetch data from {start} to {end}, status code: {response.status}")
                return []
    except Exception as e:
        logger.error(f"Error fetching batch {start} to {end}: {e}")
        return []

# Main asynchronous function to handle batch requests
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []  # List to store tasks for fetching data
        start = 0   # Start index for batch fetching

        # Loop until the flag is found
        while not flag_found.is_set():
            # Create a new task to fetch the next batch of data
            task = fetch_batch(session, start, start + batch_size)
            tasks.append(task)
            start += batch_size  # Increment start for the next batch

            # Limit the number of concurrent tasks to prevent server overload
            if len(tasks) >= 10:
                # Run the tasks concurrently and wait for completion
                results = await asyncio.gather(*tasks)

                # If no data is fetched, stop the loop
                if not any(results):
                    logger.info("No more data to fetch.")
                    break

                # Reset tasks list to avoid reusing completed tasks
                tasks = []

        # Gather remaining tasks if any and the flag is not yet found
        if tasks and not flag_found.is_set():
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
