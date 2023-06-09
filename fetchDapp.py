import streamlit as st
import streamlit.components.v1 as components

from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.aerial.wallet import LocalWallet


import base64
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from PIL import Image
import random
import pyperclip


code_title = """


st.markdown("<h1 style='text-align: center; color: blue;'>Simple Fetch.ai Web Dapp</h1>", unsafe_allow_html=True)

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

"""

code_acc_creation= """ 
with tab1:
   st.header("Create A New Fet Account Address")
   if st.button('Click to Create'):
    private_key = PrivateKey()
    st.write("Private Key: ", private_key.private_key)
    st.write(":warning: Keep it secret even from your mom :warning:")
    wallet = LocalWallet(private_key)
    st.write("Wallet Adress :", wallet)
   image = Image.open('wallet.jpg')
   st.image(image, caption='Wallet')

 """

code_wallet_recovery= """ 
with tab2:
   st.header("Create Account Address by Your Mnemonic")
   mnemonic=st.text_input('Past Wallet Mnemonic (24 Phrase): ', '')
   if st.button('Submit'):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
    wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()))
    st.write("Recovered Wallet :",wallet)
   image = Image.open('seed.jpg')
   st.image(image, caption='Mnemonic')

 """

code_check_balance= """ 
with tab3:
   st.header("Wallet Balance")
   address=st.text_input('Write Wallet Address: ', '')
   if st.button('Check'):
    ledger = LedgerClient(NetworkConfig.fetchai_mainnet())
    balance = ledger.query_bank_balance(str(address))
    st.write("Your Wallet Balance on Mainnet :", balance, "FET")

 """
code_textnet_play= code_all= """ 
with tab4:
    st.header("TestNet Playing")
    agree = st.checkbox('Agree to Create Testnet Account')
    st.write(":arrow_up: Click and...wait a few seconds...")
    if agree:
        
        your = LocalWallet.generate()
        ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
        faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())
        your_balance = ledger.query_bank_balance(your.address())
        st.write("Your Address: ", your.address())
        st.write("Your Balance: ", your_balance)
        st.write(" ")
        st.write(" ")

        url1 = "https://explore-dorado.fetch.ai/account/"+str(your.address())
        st.write("Click [link](%s) to check your account on Fetch Dorado Testnet " % url1)
  
        st.write(":moneybag: Providing wealth to you...wait a few seconds...:moneybag:")
        faucet_api.get_wealth(your.address())
        your_balance = ledger.query_bank_balance(your.address())

        
        if your_balance >0:
            st.write(" ")
            st.write(" ")
    
            st.write("Your New Balance: ", your_balance , "Fake FET tokens")
            st.balloons()
            st.write("Bad News, You can not use this fake balance :relieved: but :smiley: can testing :smiley:")
            
            url2 = "https://explore-dorado.fetch.ai/account/"+str(your.address())
            st.write("Click [link](%s) to check your account on Fetch Dorado Testnet " % url2)


        wanna = st.checkbox('wanna SEND some Tokens to your friend NOW :question: :question:')

        if wanna:
            alice = your
            bob = LocalWallet.generate()

            ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
            faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

            alice_balance = ledger.query_bank_balance(alice.address())
            st.write("Click to Send  10 FET to your friend?")
            if st.button('Send'):
                
                st.write("Just created an Address to your friend: ", bob.address())

                st.write(" ")
                
                st.write("Her/his Balance: ", ledger.query_bank_balance(bob.address()))

                st.write(" ")

                st.write("Your Balance: ", ledger.query_bank_balance(alice.address()))

                st.write(" ")
                

                tx = ledger.send_tokens(bob, 10, "atestfet", alice)
                
                st.write(" ")
                
                st.write(tx.tx_hash, "  transaction waiting to complete...")
                
                st.write(" ")
                
                tx.wait_to_complete()
                
                st.write(tx.tx_hash,  " transaction waiting to complete...done")
                

                st.write(" ")

                st.write("Her/his Balance: ", ledger.query_bank_balance(bob.address()))

                st.write("You lost 10 FET + tx fee 	:pensive:: ", ledger.query_bank_balance(alice.address()))

                url3 = "https://explore-dorado.fetch.ai/transactions/"+str(tx.tx_hash)
                st.write("Click [link](%s) to check sending setails on FeT Dorado Testnet " % url3)

"""

st.markdown("<h1 style='text-align: center; color: blue;'>Simple Fetch.ai Web Dapp</h1>", unsafe_allow_html=True)

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

with st.expander(":blue[See The Title Code]"):
    st.code(code_title, language='python')

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

tab1, tab2, tab3, tab4, tab5, tab6= st.tabs([":credit_card: Account Creation", ":unlock: Wallet Recovery", ":bank: Check Balance", ":triangular_ruler: TestNet Play", ":robot_face: AI Agents", ":chart_with_upwards_trend: Data Science"])

with tab1:
   st.header("Create A New Fet Account Address")
   if st.button('Click to Create'):
        private_key = PrivateKey()
        st.write("Private Key: ", private_key.private_key)
        st.write(":warning: Keep it secret even from your mom :warning:")
        wallet = LocalWallet(private_key)
        st.write("Wallet Adress :", wallet)
    

   with st.expander(":blue[See The Account Creation Code]"):
    st.code(code_acc_creation, language='python')

    

with tab2:
   st.header("Create Account Address by Your Mnemonic")
   mnemonic=st.text_input('Past Wallet Mnemonic (24 Phrase): ', '')
   if st.button('Submit'):
      seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
      bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
      wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()))
      st.write("Recovered Wallet :",wallet)
   with st.expander(":blue[See The Account Creation Code]"):
      st.code(code_wallet_recovery, language='python')
   



with tab3:
   st.header("Wallet Balance")
   address=st.text_input('Write Wallet Address: ', '')
   if st.button('Check'):
      ledger = LedgerClient(NetworkConfig.fetchai_mainnet())
      balance = ledger.query_bank_balance(str(address))
      st.write("Your Wallet Balance on Mainnet :", balance, "FET")
   with st.expander(":blue[See The Waallet Balance Code]"):
      st.code(code_check_balance, language='python')


   

with tab4:
    st.header("TestNet Playing")
    agree = st.checkbox('Agree to Create Testnet Account')
    st.write(":arrow_up: Click and...wait a few seconds...")
    if agree:
        
        your = LocalWallet.generate()
        ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
        faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())
        your_balance = ledger.query_bank_balance(your.address())
        st.write("Your Address: ", your.address())
        st.write("Your Balance: ", your_balance)
        st.write(" ")
        st.write(" ")

        url1 = "https://explore-dorado.fetch.ai/account/"+str(your.address())
        st.write("Click [link](%s) to check your account on Fetch Dorado Testnet " % url1)
  
        st.write(":moneybag: Providing wealth to you...wait a few seconds...:moneybag:")
        faucet_api.get_wealth(your.address())
        your_balance = ledger.query_bank_balance(your.address())

        
        if your_balance >0:
            st.write(" ")
            st.write(" ")
    
            st.write("Your New Balance: ", your_balance , "Fake FET tokens")
            st.balloons()
            st.write("Bad News, You can not use this fake balance :relieved: but :smiley: can testing :smiley:")
            
            url2 = "https://explore-dorado.fetch.ai/account/"+str(your.address())
            st.write("Click [link](%s) to check your account on Fetch Dorado Testnet " % url2)


        wanna = st.checkbox('wanna SEND some Tokens to your friend NOW :question: :question:')

        if wanna:
            alice = your
            bob = LocalWallet.generate()

            ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
            faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

            alice_balance = ledger.query_bank_balance(alice.address())
            st.write("Click to Send  10 FET to your friend?")
            if st.button('Send'):
                
                st.write("Just created an Address to your friend: ", bob.address())

                st.write(" ")
                
                st.write("Her/his Balance: ", ledger.query_bank_balance(bob.address()))

                st.write(" ")

                st.write("Your Balance: ", ledger.query_bank_balance(alice.address()))

                st.write(" ")
                

                tx = ledger.send_tokens(bob, 10, "atestfet", alice)
                
                st.write(" ")
                
                st.write(tx.tx_hash, "  transaction waiting to complete...")
                
                st.write(" ")
                
                tx.wait_to_complete()
                
                st.write(tx.tx_hash,  " transaction waiting to complete...done")
                

                st.write(" ")

                st.write("Her/his Balance: ", ledger.query_bank_balance(bob.address()))

                st.write("You lost 10 FET + tx fee 	:pensive:: ", ledger.query_bank_balance(alice.address()))

                url3 = "https://explore-dorado.fetch.ai/transactions/"+str(tx.tx_hash)
                st.write("Click [link](%s) to check sending setails on FeT Dorado Testnet " % url3)
    with st.expander(":blue[See The TestNet Play Code]"):
        st.code(code_textnet_play, language='python')
            

with tab5:
    st.header("AI Agents")
    st.write(":robot_face: Agents will visit here later :robot_face:")
    st.write("asyncio dont let to run Streamlit now due to the functipn lack of asyncio.get_event_loop() in uagents")
    st.write("Already created a discussion on Fetchai github")
    st.markdown('<a href="https://github.com/fetchai/cosmpy/discussions/360" target="_blank">Follow the discussion on Github </a>', unsafe_allow_html=True)
    st.markdown('<a href="https://discordapp.com/channels/441214316524339210/767751131110572043/1114622701072556042" target="_blank">Follow the discussion on Discord </a>', unsafe_allow_html=True)
  
    image = Image.open('robot.jpg')
    st.image(image, caption="Fet Agents")
   

with tab6:
    st.title("Data Science")
    st.write("Colearn will be here soon")
    




components.html(
    """
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
        data-text="See this cool Streamlit Fetch.ai Dapp @SelcukTopal80 #fet  #dapp #ai #blockchain🎈" 
        data-url="https://streamlit.io" 
        data-show-count="false">
        data-size="Large" 
        data-hashtags="streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
)

st.write(":coffee: :blue[Buy me a 2 Shots Americano Coffee] :coffee:")
if st.button(":red[Copy My Fet Wallet Address]"):
    text_to_be_copied = 'fetch12t9ewxmcawvh2q5hysgeezpp9gxfzzryta2k3t'
    pyperclip.copy(text_to_be_copied)
