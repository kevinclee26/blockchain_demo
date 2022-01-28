import streamlit as st
from dataclasses import dataclass
from datetime import datetime
import hashlib

st.markdown('# Welcome to Blockchain Demo')

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
        
    def hash_block(self):
        sha=hashlib.sha256()
        
        trade_time_encoded=self.trade_time.encode()
        
        sha.update(trade_time_encoded)
        
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
st.write(f'Here is the chain:\n{stockchain_live}')