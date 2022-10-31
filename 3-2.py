import requests
from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret(
    "SECRET")

# From previous lesson
sponsorKeypair=Keypair.from_secret(
    "SECRET"
)
sponsorKeypair = Keypair.random()
url = "https://friendbot.stellar.org"
frientbot_response= requests.get(url, params={"addr": sponsorKeypair.public_key})
print("sponsorKeypair public key: ", sponsorKeypair.public_key)
print("sponsorKeypair scret key: ", sponsorKeypair.secret)

# 2. Transaction
# you're a bit overeager and funded your Quest Account with the Fund button
print("Building Transaction...")
base_fee = server.fetch_base_fee()
stellar_account = server.load_account(stellar_quest_keypair.public_key)
sponsor_account = server.load_account(sponsorKeypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=sponsor_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_begin_sponsoring_future_reserves_op(
        sponsored_id=stellar_quest_keypair.public_key
    )
    .append_revoke_account_sponsorship_op(
        account_id=stellar_quest_keypair.public_key,
        source=stellar_quest_keypair.public_key
    )
    .append_end_sponsoring_future_reserves_op(
        source=stellar_quest_keypair.public_key
    )
    .append_payment_op(
        destination="GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR", #Frient bot
        asset=Asset.native(),
        amount="9999.99999",
        source=stellar_quest_keypair.public_key
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(stellar_quest_keypair)
transaction.sign(sponsorKeypair)
response = server.submit_transaction(transaction)

print("Transaction Successful! Hash: {}".format(response))