from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SBFK2ZFJD65CBELCWD6L6WJUM5F4W7MXUWULC3SE7H4VQ57WYPGTTDIM")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

print("quest_account_pub_key", quest_account_pub_key)
print("quest_account_priv_key", quest_account_priv_key)

# 2. Path
path = [
    Asset("USDT", "GAAW5ZH5FNAE2DKTCRR4VBSWR42DBIP6HS5SNIOK2MVBPDQHAA4OZHDZ"),
    Asset("BTC", "GAAW5ZH5FNAE2DKTCRR4VBSWR42DBIP6HS5SNIOK2MVBPDQHAA4OZHDZ"),
]

# 3. Transaction

print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')
transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
     .append_path_payment_strict_receive_op(
        destination="GAAW5ZH5FNAE2DKTCRR4VBSWR42DBIP6HS5SNIOK2MVBPDQHAA4OZHDZ",
        send_asset=Asset.native(),
        send_max="1000",
        dest_asset=Asset(
            "1INCH", "GAAW5ZH5FNAE2DKTCRR4VBSWR42DBIP6HS5SNIOK2MVBPDQHAA4OZHDZ"
        ),
        dest_amount=".1",
        path=path,
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")