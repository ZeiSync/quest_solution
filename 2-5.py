from email.mime import base
from stellar_sdk import Asset, Server, Keypair, Signer, TransactionBuilder, Network, TrustLineFlags
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret(
    "SECRET")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

issuer_account = Keypair.random()
base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)


# create issure account
issuer_txn = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_create_account_op(
        destination=issuer_account.public_key, starting_balance="120"
    )
    .set_timeout(30)
    .build()
)
issuer_txn.sign(stellar_quest_keypair)
res = server.submit_transaction(issuer_txn)
print("issuer_account.public_key", issuer_account.public_key)
print("Issuer account: ", res)

# Set flag
print("Building Set Flag Transaction...")
zeizei_asset = Asset(
    code="Zeizei",
    issuer=issuer_account.public_key
)
issuer = server.load_account(issuer_account.public_key)
txn = (
    TransactionBuilder(
        source_account=issuer,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee
    )
    .append_set_options_op(
        set_flags=3
    )
    .append_change_trust_op(
        asset=zeizei_asset,
        source=quest_account_pub_key
    )
    .append_set_trust_line_flags_op(
        trustor=quest_account_pub_key,
        asset=zeizei_asset,
        set_flags=TrustLineFlags(1)
    )
    .append_payment_op(
        destination=quest_account_pub_key,
        asset=zeizei_asset,
        amount='100'
    )
    .append_set_trust_line_flags_op(
        trustor=quest_account_pub_key,
        asset=zeizei_asset,
        clear_flags=TrustLineFlags(1)
    )
    .set_timeout(30)
    .build()
)
txn.sign(issuer_account)
txn.sign(quest_account_priv_key)
response = server.submit_transaction(txn)

print("response: ", response)
