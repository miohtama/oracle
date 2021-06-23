"""Run Merke distributor once.

Useful for diagnosing issues with Ethereunm 1.0 JSON-RPC connectivity.
"""
import logging

from eth_typing import BlockNumber

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
    MAX_TX_WAIT_SECONDS, ETH1_CONFIRMATION_BLOCKS,
)

from src.utils import (
    get_latest_block_number,
    check_oracle_has_vote,
    wait_for_oracles_nonce_update,
    check_default_account_balance,
)

from src.merkle_distributor.utils import (
    get_merkle_root_voting_parameters,
    get_reth_disabled_accounts,
    get_prev_merkle_root_parameters,
    get_merkle_distributor_claimed_addresses,
    get_unclaimed_balances,
    get_distributions,
    get_oracles_config,
    get_staked_eth_period_reward,
    Distribution,
    get_staked_eth_distributions,
    get_ens_node_id,
    OraclesSettings,
    get_merkle_node,
    pin_claims_to_ipfs,
    submit_oracle_merkle_root_vote,
    Rewards,
)

from src.utils import (
    get_web3_client,
)

logger = logging.getLogger(__name__)

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
# merkle_distributor.process()

current_block_number: BlockNumber = get_latest_block_number(
    w3=web3_client, confirmation_blocks=ETH1_CONFIRMATION_BLOCKS
)

logger.info("get_merkle_root_voting_parameters")
(
    is_voting,
    is_paused,
    current_nonce,
    new_rewards_block_number,
) = get_merkle_root_voting_parameters(
    oracles=merkle_distributor.oracles,
    multicall=merkle_distributor.multicall_contract,
    reward_eth_token=merkle_distributor.reward_eth_token,
    block_number=current_block_number,
)


logger.info("get_prev_merkle_root_parameters")
prev_merkle_root_parameters = get_prev_merkle_root_parameters(
    merkle_distributor=merkle_distributor.merkle_distributor,
    reward_eth_token=merkle_distributor.reward_eth_token,
    to_block=new_rewards_block_number,
)
