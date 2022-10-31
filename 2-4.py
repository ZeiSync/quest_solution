import requests
from stellar_sdk import Asset, Server, Keypair, Signer, TransactionBuilder, Network

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret(
    "SECRET")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

random_keypair_one = Keypair.random()
url = "https://friendbot.stellar.org"
frientbot_response_one = requests.get(url, params={"addr": random_keypair_one.public_key})
print("random_keypair_one public key: ", random_keypair_one.public_key)
print("random_keypair_one scret key: ", random_keypair_one.secret)
secondary_singer = Signer.ed25519_public_key(
    account_id=random_keypair_one.public_key,
    weight=2
)

random_keypair_two = Keypair.random()
frientbot_response_two = requests.get(url, params={"addr": random_keypair_two.public_key})
print("random_keypair_two public key: ", random_keypair_two.public_key)
print("random_keypair_two scret key: ", random_keypair_two.secret)
third_signer = Signer.ed25519_public_key(
    account_id=random_keypair_two.public_key,
    weight=2
)

# 3. Transaction
# print("Building Transaction...")
base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_set_options_op(
        master_weight=1,
        low_threshold=5,
        med_threshold=5,
        high_threshold=5
    )
    .append_set_options_op(signer=secondary_singer)
    .append_set_options_op(signer=third_signer)
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')

transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")

print('transaction payment...')

payment_txn = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_payment_op(
        destination="GCT562BOMNE2XSQK5HXQXJLSPGYT7WMJLDSPQW42GVUZM3V3HQEPBWH2",
        asset=Asset.native(),
        amount="100"
    )
    .set_timeout(30)
    .build()
)
payment_txn.sign(stellar_quest_keypair)
payment_txn.sign(random_keypair_one)
payment_txn.sign(random_keypair_two)

payment_response = server.submit_transaction(payment_txn)

print(f"Payment_response: {payment_response}")

