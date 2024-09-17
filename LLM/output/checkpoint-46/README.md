---
library_name: peft
---
## Training procedure


The following `bitsandbytes` quantization config was used during training:
- quant_method: QuantizationMethod.BITS_AND_BYTES
- _load_in_8bit: False
- _load_in_4bit: True
- llm_int8_threshold: 6.0
- llm_int8_skip_modules: None
- llm_int8_enable_fp32_cpu_offload: False
- llm_int8_has_fp16_weight: False
- bnb_4bit_quant_type: fp4
- bnb_4bit_use_double_quant: False
- bnb_4bit_compute_dtype: float32
- bnb_4bit_quant_storage: uint8
- load_in_4bit: True
- load_in_8bit: False
### Framework versions


- PEFT 0.5.0
