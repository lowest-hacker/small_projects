import requests
import time

def complete_ticktick_task(task_id, project_id, token):
    # List to collect error messages for logging
    err = []
    # Flag to record successful completion
    success = False
    # Attempt a maximum of 5 times
    for i in range(5):
        # Post request, completing a task requires no payload according to documentation
        res = requests.post(
            f"https://api.ticktick.com/open/v1/project/{project_id}/task/{task_id}/complete",
            headers={"Authorization": f"Bearer {token}"}
        )
        try:
            res.raise_for_status()
            # On valid successful response, log and return data
            print(res.json())
            # Log any errors that may have occurred in previous attempts
            if err:
                print(f"Failed {len(err)} times, error messages follow")
                for errMsg in err:
                    print(errMsg)
            # Exit function on valid response
            success = True
            return res
        except requests.exceptions.HTTPError as e:
            # Log response and push response to errors
            err.append(f"{res.status_code}: {res.reason}")
            print(f"{res.status_code}: {res.reason}")
        except Exception as e:
            # Log other exceptions
            errorMessage = str(e)
            print(errorMessage)
            err.append(errorMessage)
        # Exit function on valid response
        if success:
            return res
        # Exponential 2s backoff: (2-4-8-16-32) second delays
        time.sleep(2 ** (i + 1))

    # Log all errors to error console
    print("Error occurred, could not complete task in 5 attempts. Error messages follow.")
    for errorMessage in err:
        print(errorMessage)
    # Return error array on failure
    return err
