"""Run Merke distributor once.

Useful for diagnosing issues with Ethereunm 1.0 JSON-RPC connectivity.
"""
import logging
from src.merkle_distributor.distributor import Distributor
from src.settings import (
    WEB3_WS_ENDPOINT,
    WEB3_WS_ENDPOINT_TIMEOUT,
    WEB3_HTTP_ENDPOINT,
    INJECT_POA_MIDDLEWARE,
    INJECT_STALE_CHECK_MIDDLEWARE,
    INJECT_RETRY_REQUEST_MIDDLEWARE,
    INJECT_LOCAL_FILTER_MIDDLEWARE,
    STALE_CHECK_MIDDLEWARE_ALLOWABLE_DELAY,
    APPLY_GAS_PRICE_STRATEGY,
    MAX_TX_WAIT_SECONDS,
)

from src.utils import (
    get_web3_client,
)

logging.basicConfig(
    format="%(name)-12s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
)

web3_client = get_web3_client(
    http_endpoint=WEB3_HTTP_ENDPOINT,
    ws_endpoint=WEB3_WS_ENDPOINT,
    ws_endpoint_timeout=WEB3_WS_ENDPOINT_TIMEOUT,
    apply_gas_price_strategy=APPLY_GAS_PRICE_STRATEGY,
    max_tx_wait_seconds=MAX_TX_WAIT_SECONDS,
    inject_retry_request=INJECT_RETRY_REQUEST_MIDDLEWARE,
    inject_poa=INJECT_POA_MIDDLEWARE,
    inject_local_filter=INJECT_LOCAL_FILTER_MIDDLEWARE,
    inject_stale_check=INJECT_STALE_CHECK_MIDDLEWARE,
    stale_check_allowable_delay=STALE_CHECK_MIDDLEWARE_ALLOWABLE_DELAY,
)
merkle_distributor = Distributor(w3=web3_client)
merkle_distributor.process()