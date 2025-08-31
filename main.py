from openai import OpenAI
from dotenv import find_dotenv,load_dotenv
import os
import time
import logging
from datetime import datetime
# Load all environment variable

load_dotenv()

# Fetch the OPENAI API KEY and assign it to api_key

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI()
Model = "gpt-4"

# Create an Assistant
personal_trainer_assistant = client.beta.assistants.create(
    name= "Personal Trainer",
    instructions="""
    You are the best personal trainer and nutritionist who knows how to get clients build the lean muscles.
    You have trained high caliber athletes and movie stars""",
    model= Model)

Assistant_id = personal_trainer_assistant.id
print(Assistant_id)

#create a thread for the Assistant

thread = client.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content":"What food should I eat to build muscles"
        }
    ]
)
thread_id = thread.id
print(thread_id)

#User message to converse with the petrsonal_trainer Assistant

message = "what are the best exercises to build lean muscles and getting stronger?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

run = client.beta.threads.runs.create(
    assistant_id=Assistant_id,
    thread_id=thread_id,
    instructions="Please address the user as James Bond"

)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")