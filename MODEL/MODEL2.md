train.py : 


model = PerceiverAR(
    num_tokens = 1250,
    dim = 2048,
    depth = 32,
    ff_mult=2,
    cross_attn_dropout = 0.3,
    max_seq_len = SEQ_LEN,
    cross_attn_seq_len = PREFIX_SEQ_LEN
)

perceiver_ar_python_full.py

class CausalAttention(nn.Module):
    def __init__(
        self,
        *,
        dim,
        dim_head = 64,
        heads = 16,
        dropout = 0.3
    ):



class CausalPrefixAttention(nn.Module):
    def __init__(
        self,
        *,
        dim,
        dim_head = 64,
        heads = 16,
        max_heads_process = 2,
        dropout = 0.3,
        cross_attn_dropout = 0.3
    ):



class PerceiverAR(nn.Module):
    def __init__(
        self,
        *,
        num_tokens,
        dim,
        depth,
        max_seq_len,
        cross_attn_seq_len,
        dim_head = 64,
        heads = 16,
        dropout = 0.3,
        cross_attn_dropout = 0.3,
        ff_mult = 4,
        perceive_depth = 1,
        perceive_max_heads_process = 2 # processes the heads in the perceiver layer in chunks to lower peak memory, in the case the prefix is really long
    ):


    class AutoregressiveWrapper(nn.Module):
    def __init__(self, net, pad_value=0):
        super().__init__()
        self.max_seq_len = net.max_seq_len
        self.pad_value = pad_value
        self.net = net

    @torch.no_grad()
    @eval_decorator
    def generate(
        self,
        start_tokens,
        seq_len,
        eos_token=None,
        temperature=1.0,
        filter_thres=0.9,
        verbose=True,
        return_prime=True,
        **kwargs
    ):