# greek_scraper/gpu_processor.py
import cupy as cp
import numpy as np

greek_filter_kernel = cp.ElementwiseKernel(
    'uint32 raw_chars',  # 'raw unsigned int chars' 대신 'uint32 raw_chars' 사용
    'bool is_greek',
    '''
    const unsigned int c = raw_chars[i]; // 'uint32' 대신 'unsigned int' 사용
    is_greek = (c >= 0x0370 && c <= 0x03FF) ||  // Basic Greek
        (c >= 0x1F00 && c <= 0x1FFF);  // Extended Greek
        // Emoji range removed for generic use, add back if needed for emoji removal:
        // || (c >= 0x1F600 && c <= 0x1F64F);       // Emoji (to remove) - Removed for generic scraper
    ''',
    'greek_filter'
)

class GPUTextProcessor:
    def __init__(self):
        self.stream = cp.cuda.Stream()  # Use CUDA stream for async execution

    def process_batch(self, texts):
        try:
            code_points = [np.array([ord(c) for c in t], dtype=np.uint32) for t in texts]
            lengths = [len(arr) for arr in code_points]
            max_len = max(lengths) if lengths else 0

            if max_len == 0:
                return texts  # Avoid processing empty inputs

            with self.stream:  # Asynchronous execution
                gpu_buffer = cp.zeros((len(texts), max_len), dtype=cp.uint32)
                for i, arr in enumerate(code_points):
                    gpu_buffer[i, :len(arr)] = cp.asarray(arr)

                mask = greek_filter_kernel(gpu_buffer)
                cleaned_texts = [
                    ''.join(chr(c) for c in gpu_buffer[i][mask[i, :len(code_points[i])]].get() if c != 0)
                    for i in range(len(texts))
                ]

            cp.cuda.Device(0).synchronize()  # Ensure GPU execution completes before returning
            return cleaned_texts
        except Exception as e:
            return texts  # Fallback to original input if GPU fails