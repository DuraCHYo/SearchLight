# SearchLight

This README also available in [Русском](README-RU.md)

SearchLight is a command-line interface (CLI) tool designed for managing and interacting with OpenSearch clusters. It provides a structured and extensible way to perform administrative and operational tasks such as security management, index policies handling, cluster monitoring, and more.
Planned as OpenSearch-SwissKnife in OpenSearch APIs world.

The project is built using `typer` for CLI handling and leverages the official `opensearch-py` client.

## Features

- Security management (users, roles)
- Index policy management
- Cluster task inspection and control
- Node information retrieval
- Unified CLI interface for OpenSearch operations
- Modular and extensible architecture

## Architecture

The project follows a modular design that separates concerns between CLI, business logic, and infrastructure:

```
searchlight/
├── main.py              # CLI entry point
├── cli.py               # Command definitions
├── client.py            # OpenSearch client initialization
├── core/                # Core operations (e.g., backup, restore)
├── services/            # OpenSearch interaction layer
│   ├── security.py
│   ├── index_management.py
│   ├── tasks.py
│   ├── nodes.py
│   └── templates.py
├── utils/               # Utilities (logging, formatting, helpers)
```

### Components Overview

- **CLI Layer**: Defines commands and arguments using Typer
- **Services Layer**: Encapsulates OpenSearch API interactions
- **Client Layer**: Handles connection configuration
- **Core Layer**: Implements higher-level operations
- **Utils**: Shared utilities such as logging and formatting

## Installation

Clone the repository:

```bash
git clone https://github.com/DuraCHYo/SearchLight.git
cd SearchLight
```

Install dependencies using Poetry:

```bash
poetry install
```

Alternatively, install via pip:

```bash
pip install .
```

## Configuration

SearchLight supports configuration via CLI arguments and environment variables.

Common parameters include:

- `--host` (or `OS_HOST`)
- `--port` (or `OS_PORT`)
- `--auth` (format: `username:password`)
- SSL-related options

Example:

```bash
searchlight --host localhost --port 9200 --auth admin:admin
```

## Usage

### Security Operations

```bash
searchlight security ...
```

Manage users and roles within the OpenSearch cluster.

### Index Policies

```bash
searchlight policies ...
```

Create, update, or inspect index management policies.

### Cluster Tasks

```bash
searchlight tasks ...
```

View and manage running tasks.

### Node Information

```bash
searchlight nodes ...
```

Retrieve information about cluster nodes.

## Testing

Run the test suite using:

```bash
pytest
```

## Contributing

Contributions are welcome and encouraged.

To contribute:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Ensure code quality:
   - Follow existing project structure
   - Write or update tests if necessary
5. Run tests locally:
   ```bash
   pytest
   ```
6. Commit your changes:
   ```bash
   git commit -m "Add: description of changes"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a Pull Request

### Code Style

- Follow PEP8 guidelines
- Keep functions small and focused
- Prefer explicit over implicit behavior
- Maintain clear separation between CLI and business logic

## Extending the Project

To add new functionality:

1. Implement logic inside `services/`
2. Expose it via CLI in `cli.py`
3. Reuse utilities and client where applicable

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.