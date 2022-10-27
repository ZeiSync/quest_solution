from unicodedata import name
from stellar_sdk import Account, Asset, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret(
    "SECRET")

# 3. Transaction
print("Building Transaction...")
base_fee = server.fetch_base_fee()
stellar_account = server.load_account(stellar_quest_keypair.public_key)
print(stellar_account.sequence)
transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_bump_sequence_op(
        bump_to=stellar_account.sequence + 100
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(stellar_quest_keypair.secret)
response = server.submit_transaction(transaction)

print("Transaction Successful! Hash: {}".format(response))

# --- transction 2 ---
bumpedAccount = Account(stellar_quest_keypair.public_key,  stellar_account.sequence + 99)

next_txn = (
    TransactionBuilder(
        source_account=bumpedAccount,
        base_fee=base_fee,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
    ).append_manage_data_op(
        data_name="bumped",
        data_value="hahaha"
    )
    .set_timeout(30)
    .build()
)

next_txn.sign(stellar_quest_keypair)
nextRes = server.submit_transaction(next_txn)