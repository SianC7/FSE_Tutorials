# Tutorial 10: Interprocess Communication with Message Queues 

In this tutorial, you'll learn about interprocess communication (IPC) using message queues. Message queues allow different processes to communicate and synchronize their actions by sending and receiving messages asynchronously. Previously we created the financial charts every time a user requested the dashboard, which can be slow. Now, we'll offload chart generation to a background worker using a message queue, improving responsiveness. 

### Learning Objectives

- Understand the concept of interprocess communication (IPC) and message queues.
- Learn how to set up a message queue using Celery and Redis.
- Work with Docker and Docker Compose to orchestrate multiple services.
- Implement asynchronous task processing in a web application.

---

## What is Interprocess Communication (IPC)?

**Interprocess Communication (IPC)** is a mechanism that allows different processes (programs running independently) to communicate and share data with each other. In modern applications, IPC is essential for building scalable, distributed systems where multiple components work together.

### Common IPC Mechanisms:
- **Pipes and Named Pipes**: Direct communication channels between processes
- **Shared Memory**: Multiple processes access the same memory space
- **Message Queues**: Processes send and receive messages asynchronously
- **Sockets**: Network-based communication between processes

### Benefits of IPC with Message Queues:

1. **Asynchronous Processing**: The main application doesn't wait for slow tasks to complete
2. **Decoupling**: Services can be developed, deployed, and scaled independently
3. **Reliability**: Messages can be persisted, ensuring tasks aren't lost if a worker crashes
4. **Scalability**: Multiple workers can process tasks from the same queue
5. **Load Balancing**: Work is automatically distributed across available workers

---

## What is a Message Queue?

A **message queue** is a form of asynchronous service-to-service communication. Messages (tasks) are placed in a queue, and worker processes retrieve and execute them. This pattern is ideal for:

- Long-running tasks (generating reports, processing images, sending emails)
- Background jobs that don't need immediate results
- Tasks that can be retried if they fail

### How It Works:

1. **Producer** (your Flask app): Sends tasks to the queue
2. **Message Broker** (Redis): Stores tasks and manages the queue
3. **Consumer/Worker** (Celery workers): Retrieves and executes tasks
4. **Result Backend** (Redis): Stores task results for retrieval

```
[Flask App] --task--> [Redis Queue] --task--> [Celery Worker]
                           ^                        |
                           |                    result
                           +------------------------+
```

---

## Celery and Redis Overview

### What is Celery?

**Celery** is a distributed task queue framework for Python. It allows you to:
- Define tasks as regular Python functions
- Execute tasks asynchronously in background workers
- Schedule periodic tasks (like cron jobs)
- Monitor task execution and retrieve results

### What is Redis?

**Redis** (Remote Dictionary Server) is an in-memory data structure store that can be used as:
- A **message broker**: Stores task messages in a queue
- A **result backend**: Stores task results
- A **cache**: Fast key-value storage

Redis is perfect for message queuing because:
- It's extremely fast (in-memory storage)
- Supports pub/sub and list data structures ideal for queues
- Provides persistence options to prevent data loss

### Benefits of Using Celery with Redis:

1. **Simple Setup**: Minimal configuration required
2. **High Performance**: Redis's in-memory architecture ensures low latency
3. **Flexible Task Management**: Support for task priorities, retries, and timeouts
4. **Monitoring**: Built-in tools to monitor task execution
5. **Scalability**: Easy to add more workers as load increases

---

## Docker and Docker Compose Setup

To run our application with multiple services (Flask app, Celery workers, Redis), we use **Docker** and **Docker Compose**.

### What is Docker?

**Docker** is a containerization platform that packages applications and their dependencies into isolated containers. Each container:
- Runs consistently across different environments
- Is isolated from other containers and the host system
- Can be started, stopped, and scaled independently

### What is Docker Compose?

**Docker Compose** is a tool for defining and running multi-container Docker applications. With a single YAML file (`docker-compose.yml`), you can:
- Define all services (web app, workers, database, cache)
- Configure networking between services
- Manage volumes for persistent data
- Start/stop all services with one command

### Our Application Architecture:

```
┌─────────────────┐
│   Flask Web     │  Port 5000 - Web interface
│   Application   │
└────────┬────────┘
         │
         ├──────────> [Redis] Port 6379 - Message broker & result backend
         │               │
         │               ├──> [Celery Worker 1] - Processes tasks
         │               │
         │               └──> [Celery Beat] - Schedules periodic tasks
         │
└────────┴────────┘
  Shared Volume
  (code & database)
```

---

## Installation Instructions

### Prerequisites

1. **Install Docker Desktop**:
   - **Windows**: Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - **macOS**: Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) ✓
   - **Linux**: Install Docker Engine and Docker Compose:
     ```bash
     sudo apt-get update
     sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
     ```

2. **Verify Installation**: ✓
   ```bash
   docker --version
   docker-compose --version
   ```

### Project Setup

1. **Navigate to Project Directory**:✓
   ```bash
   cd FSE_Tutorials
   ```

2. **Build and Start Services**:✓
   ```bash
   docker-compose up --build
   ```

   This command:
   - Builds Docker images for your application
   - Starts Redis, Flask app, Celery worker, and Celery beat
   - Shows logs from all services in your terminal

3. **Run in Background (Detached Mode)**:✓
   ```bash
   docker-compose up -d
   ```

4. **View Logs**:✓
   ```bash
   docker-compose logs -f
   ```

5. **Stop Services**:✓
   ```bash
   docker-compose down
   ```

6. **Access the Application**:✓
   - Open browser to `http://127.0.0.1:5001`
   - The Flask app will connect to Redis automatically

---

## What We've Already Implemented

The codebase already includes several Celery tasks and integration with the Flask application. Here's what's been done:

### Celery Configuration (`tasks.py`)

One task is implemented:

#### **Chart Generation Task** (Asynchronous with Result)
```python
@celery.task(name="generate_charts_task")
def generate_charts_task():
    """Generates financial charts asynchronously."""
    # Returns paths to generated chart images
```

- **Purpose**: Generate expense and income pie charts
- **Type**: Async task that returns results (stored in Redis)
- **Used in**: Dashboard route - triggered when user loads the page
- **Polling**: Frontend polls `/api/chart-status/<task_id>` to check completion

---

## Your Task: Implement the Audit Logging Function

The `log_transaction_audit_task` function is currently a placeholder. Your task is to implement it so that it logs transaction audit information to a file named `transaction_audit.log`.

### Requirements

1. Open `tasks.py` and implement the `log_transaction_audit_task` function:✓
   - Retrieve the transaction details using the provided `transaction_id`
   - Log the transaction information (ID, amount, type, timestamp) to `transaction_audit.log`
   - Handle cases where the transaction ID is not found and log an appropriate error message
2. Update `apps.py` to call this task after adding a transaction.✓

There are `TODO` comments in `tasks.py` and `app.py` to guide you.


### Testing Your Implementation

```bash
# Run tests as before.
pytest tests/
```

---

## Key Concepts Review

### Task Execution Flow

1. **Flask app** calls `task_name.delay(args)` - puts task in Redis queue
2. **Redis** stores the task message
3. **Celery worker** retrieves the task from Redis
4. **Worker** executes the task function
5. **Result** (if any) is stored back in Redis
6. **Flask app** can retrieve the result using the task ID

### When to Use Async Tasks

✅ **Use async tasks for**:
- Long-running operations (> 1 second)
- Non-critical background work
- Tasks that can fail and retry
- Operations that don't need immediate results

❌ **Don't use async tasks for**:
- Quick operations (< 100ms)
- Critical real-time data needed immediately
- Simple database queries
- User authentication/authorization

### Debugging Tips

1. **Check Redis Connection**:
   ```bash
   docker exec -it fse_redis redis-cli ping
   # Should return: PONG
   ```

2. **View Celery Logs**:
   ```bash
   docker-compose logs -f celery_worker
   ```

3. **Inspect Task State** (in Python):
   ```python
   from tasks import generate_charts_task
   task = generate_charts_task.AsyncResult('task-id-here')
   print(task.state)  # PENDING, SUCCESS, FAILURE, etc.
   print(task.result)  # Task return value
   ```

4. **Common Issues**:
   - **Task not executing**: Check if Celery worker is running
   - **Connection refused**: Ensure Redis is running and accessible
   - **Task ID is None**: Make sure you committed the transaction before passing its ID

---

## Additional Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Async Patterns](https://flask.palletsprojects.com/en/latest/patterns/celery/)

---

## Submission

1. Complete the test implementation in `tests/test_log_transaction_audit.py`
2. Run the tests and ensure they pass
3. Verify the application works:
   - Start services: `docker-compose up`
   - Add a transaction via the web interface

Good luck! 🚀
