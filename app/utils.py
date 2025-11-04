from typing import List
 
#package for "regular expression"
import re

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    if chunk_size<= 0:
        chunk_size =1200
    if overlap >=chunk_size:
        overlap= max(0, int(0.2 * chunk_size))

    chunks =[]
    start =0
    n =len(text)
    step=max(1, chunk_size - overlap)

    # Minimize chunks for a more opti app but you can remove it if you have enough calculus power
    MAX_CHUNKS=20000

    while start < n and len(chunks) <MAX_CHUNKS:
        end =min(start+chunk_size,n )
        chunks.append( text[start:end])
        start +=step
    return chunks



def clean_text(s: str )-> str:
    s =re.sub(r"\s+", " " ,s)
    return s.strip()
