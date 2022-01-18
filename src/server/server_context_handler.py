from context.app_state import AppState


def on_client_connected():
    AppState._instance.number_of_connected_clients += 1
    print(
        f'on_client_connected: \
        {AppState._instance.number_of_connected_clients}'
    )


def on_client_disconnected():
    AppState._instance.number_of_connected_clients -= 1
    print(
        f'on_client_disconnected: \
        {AppState._instance.number_of_connected_clients}'
    )
