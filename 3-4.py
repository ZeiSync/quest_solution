from stellar_sdk import  Asset, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SECRET")
stellar_account = server.load_account(stellar_quest_keypair.public_key)
print("stellar_quest public key: ", stellar_quest_keypair.public_key)
print("stellar_quest scret key: ", stellar_quest_keypair.secret)

# 2. Transaction
print("Building Transaction...")
base_fee = server.fetch_base_fee()

clawback_asset = Asset(
    code="clawback",
    issuer=stellar_quest_keypair.public_key
)

transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_set_options_op(
        set_flags=10
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(stellar_quest_keypair)
response = server.submit_transaction(transaction)

print("Transaction Successful! Hash: {}".format(response))