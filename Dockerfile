# Step 1: Use a base Python image
FROM python:3.13-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file (if any) and the bot script
COPY requirements.txt ./
COPY tristaprogrammista_bot.py ./

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Set environment variable for bot token (optional)
# Uncomment if you want to provide a default token here
# ENV TRISTA_BOT_TOKEN="your_default_token_here"

# Step 6: Define the command to run your bot
CMD ["python", "tristaprogrammista_bot.py"]