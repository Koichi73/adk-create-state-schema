# create-state-schema

An ADK (Agent Development Kit) plugin that automatically generates a state schema from agent state changes. It tracks `state_delta` events and builds a JSON schema describing each state key's type, length, and originating agent.

## Setup

```bash
uv sync
```

Set up Google Cloud credentials (Vertex AI):

```bash
gcloud auth application-default login
```

## Usage

### CLI

```bash
uv run adk run sample_agent
```

### Web UI

```bash
uv run adk web
```

## Example

Input: `hello`

Expected output:

```json
{
  "current_time": {
    "generated_agent": "root_agent",
    "type": "str",
    "length": 8
  },
  "greeting": {
    "generated_agent": "root_agent",
    "type": "str",
    "length": 62
  }
}
```

## How It Works

The `CreateStateSchema` plugin hooks into ADK's event system via `on_event_callback`. When a `state_delta` is detected, it records metadata (agent name, value type, length) for each key and stores the resulting schema back into session state under `state_schema`.
