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
        self.stream = cp.cuda.Stream()

    def process_batch(self, texts):
        print("[GPUTextProcessor] Processing BATCH of texts on GPU...")
        try:
            with self.stream:
                code_points = [np.array([ord(c) for c in t], dtype=np.uint32) for t in texts]
                lengths = [len(arr) for arr in code_points]
                max_len = max(lengths) if lengths else 0
                gpu_buffer = cp.zeros((len(texts), max_len), dtype=cp.uint32)
                for i, arr in enumerate(code_points):
                    gpu_buffer[i, :len(arr)] = cp.asarray(arr)
                mask = greek_filter_kernel(gpu_buffer)
                cleaned_texts = []
                for i in range(len(texts)):
                    filtered = gpu_buffer[i][mask[i, :len(code_points[i])]].get()
                    cleaned = ''.join([chr(c) for c in filtered if c != 0])
                    cleaned_texts.append(cleaned)
            print("[GPUTextProcessor] Finished GPU batch processing.")
            return cleaned_texts # Explicit return
        except Exception as e:
            print(f"[GPUTextProcessor] ERROR during batch processing: {e}")
            return None # Explicitly return None in case of error