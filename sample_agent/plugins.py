from google.adk.plugins.base_plugin import BasePlugin
from google.adk.events import Event, EventActions
import time

class CreateStateSchema(BasePlugin):
    def __init__(self) -> None:
        super().__init__(name="create_state_schema")
        self.event_count = 0 # for log

    async def on_event_callback(self, invocation_context, event):
        # Event callback log
        self.event_count += 1
        print(f"[Event Callback Log] Event Count: {self.event_count}, Agent Name: {invocation_context.agent.name}")
        print(f"State: {invocation_context.session.state}")

        if event.actions.state_delta:
            state_delta = event.actions.state_delta
            print(f"State Delta: {state_delta}")

            # Get the current state_schema
            current_schema = dict(invocation_context.session.state.get("state_schema", {}))

            # Define state changes
            for key, value in state_delta.items():
                # Skip keys starting with "temp:" and "state_schema"
                if key.startswith("temp:") or key == "state_schema":
                    continue
                current_schema[key] = {
                    "generated_agent": invocation_context.agent.name,
                    "type": type(value).__name__,
                    "length": len(value) if hasattr(value, "__len__") else None,
                }

            state_changes = {"state_schema": current_schema}

            # Create Event with Actions
            actions_with_update = EventActions(state_delta=state_changes)

            system_event = Event(
                invocation_id=f"{invocation_context.invocation_id}_state_schema_updated",
                author="system",
                actions=actions_with_update,
                timestamp=time.time()
            )

            # Append the Event
            session_service = invocation_context.session_service
            session = invocation_context.session
            await session_service.append_event(session, system_event)

        print(f"Updated State: {invocation_context.session.state}")
