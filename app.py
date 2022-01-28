import streamlit as st
from dataclasses import dataclass
from datetime import datetime
import hashlib

st.markdown('# Welcome to Blockchain Demo')

input_buyer_id=st.text_input('Buyer ID')
input_seller_id=st.text_input('Seller ID')
input_shares=st.text_input('Shares')

@dataclass
class RecordTrade():
    buyer_id: str
    seller_id: str
    shares: float

@dataclass
class Block():
    record: RecordTrade
    trade_time: str=datetime.utcnow().strftime('%H:%M:%S')
    prev_hash: str='0'
    hash: str='0'
        
    def hash_block(self):
        sha=hashlib.sha256()
        
        trade_time_encoded=self.trade_time.encode()
        
        sha.update(trade_time_encoded)
        
        block_hash=sha.hexdigest()
        self.hash=block_hash
        return sha.hexdigest()

from typing import List

@dataclass
class StockChain():
    chain: List[Block]
        
    def add_block(self, block):
        self.chain=self.chain+[block]

@st.cache(allow_output_mutation=True)
def setup():
    chain=StockChain(
            chain=[Block(
                record=RecordTrade(
                    buyer_id=1,
                    shares=100,
                    seller_id=2
                )
            )]
    )
    return chain

stockchain_live=setup()

if st.button('Add Block'): 
    last_block=stockchain_live.chain[-1]
    prev_block_hash=last_block.hash_block()
    new_block=Block(
                record=RecordTrade(
                    buyer_id=input_buyer_id, 
                    seller_id=input_seller_id, 
                    shares=input_shares
                    ), 
                prev_hash=prev_block_hash
                )
    stockchain_live.add_block(new_block)
    st.write(f'Here is the chain:\n{stockchain_live}')