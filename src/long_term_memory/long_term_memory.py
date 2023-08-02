
from .chromadb import add_chunks_to_collector, make_collector 
import typing
params = {
    'chunk_count': 5,
    'chunk_count_initial': 10,
    'time_weight': 0,
    'chunk_length': 700,
    'chunk_separator': '',
    'strong_cleanup': False,
    'threads': 4,
    'exchange_length': 2
}

collector = make_collector()

def chunk_history(message_history: typing.List[str]) -> typing.List[str]:
    return ["\n".join(message_history[i:i + params['exchange_length']]) for i in range(0, len(message_history), params['exchange_length'])]

def get_memories(message_history: typing.List[str]) -> str:
    #get any relevant memories
    memories = collector.get_sorted(message_history, n_results=params['chunk_count'])
    #insert the current history into the memory database
    chunks = chunk_history(message_history)
    add_chunks_to_collector(chunks, collector)
    return "\n".join(memories)