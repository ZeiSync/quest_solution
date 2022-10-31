from stellar_sdk import  Asset, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SECRET")
stellar_account = server.load_account(stellar_quest_keypair.public_key)
print("stellar_quest public key: ", stellar_quest_keypair.public_key)
print("stellar_quest scret key: ", stellar_quest_keypair.secret)

destination_keypair = Keypair.random()
url = "https://friendbot.stellar.org"
frientbot_response = requests.get(url, params={"addr": destination_keypair.public_key})
print("destination_keypair public key: ", destination_keypair.public_key)
print("destination_keypair scret key: ", destination_keypair.secret)


# 2. Transaction
print("Building Transaction...")
base_fee = server.fetch_base_fee()

print("Start creating asset")
clawback_asset = Asset(
    code="clawback",
    issuer=stellar_quest_keypair.public_key
)

txn = (
    TransactionBuilder(
        source_account=stellar_account,
        base_fee=base_fee,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
    )
    .append_set_options_op(
        set_flags=10
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
txn.sign(stellar_quest_keypair)
set_flag_res = server.submit_transaction(txn)
print("set_flag_response: ", set_flag_res)


print("Making to created asset")
payment_txn = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_change_trust_op(
        asset=clawback_asset,
        source=destination_keypair.public_key
    )
    .append_payment_op(
        destination=destination_keypair.public_key,
        asset=clawback_asset,
        amount="500"
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
payment_txn.sign(stellar_quest_keypair)
payment_txn.sign(destination_keypair)
response = server.submit_transaction(payment_txn)
print("Transaction Successful! Hash: {}".format(response))


# Clawback transaction
print("Clawback Asset")
clawback_txn = (
    TransactionBuilder(
        source_account=stellar_account,
        base_fee=base_fee,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
    )
    .append_clawback_op(
        asset=clawback_asset,
        amount="250",
        from_= destination_keypair.public_key
    )
    .set_timeout(30)
    .build()
)

print("Siging Clawback Transaction")
clawback_txn.sign(stellar_quest_keypair)
clawback_txn_res = server.submit_transaction(clawback_txn)

print("clawback_txn_res", clawback_txn_res)