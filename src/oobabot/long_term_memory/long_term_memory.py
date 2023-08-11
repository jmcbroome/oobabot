
from .chromadb import add_chunks_to_collector, make_collector 
import typing
params = {
    'chunk_count': 3,
    'max_length': 700,
    'exchange_length': 2
}

collector = make_collector()

def chunk_history(message_history: typing.List[str]) -> typing.List[str]:
    return ["\n".join(message_history[i:i + 1 + params['exchange_length']]) for i in range(0, len(message_history), params['exchange_length'])]

def get_memories(message_history: typing.List[str], max_length: int = 3000) -> typing.List[str]:
    #get any relevant memories
    memories = collector.get_sorted(message_history, n_results=params['chunk_count'])
    #insert the current history into the memory database
    chunks = chunk_history(message_history)
    add_chunks_to_collector(chunks, collector)
    #remove memories over the maximum context length
    if max_length > 0:
        memlengths = [len(m) for m in memories]
        cumulative = 0
        top_index = 0
        for ti, ml in enumerate(memlengths):
            cumulative += ml
            top_index = ti
            if cumulative > max_length:
                break
        memories = memories[:top_index] #excludes the top index 
        #clean up separators before returning memory string
        return [m.strip() for m in memories]
    else:
        #if we don't have any space, return nothing.
        return []
