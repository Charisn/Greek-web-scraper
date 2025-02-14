# greek_scraper/pipelines.py
import json
from itemadapter import ItemAdapter # Import if not already in your pipelines.py
from greek_scraper.gpu_processor import GPUTextProcessor # Import GPU Processor
from twisted.internet.threads import deferToThread # Ensure this is imported if you moved it
import unicodedata

class TextPipeline:
    def __init__(self, use_cpu=False, target_language=None): # Accept use_cpu and target_language in init
        self.use_cpu = use_cpu
        self.target_language = target_language
        if not self.use_cpu:
            self.gpu_processor = GPUTextProcessor()
        else:
            self.gpu_processor = None # No GPU processor in CPU mode
            print("[TextPipeline] GPU processing disabled (CPU mode).")
        self.batch = []
        self.batch_size = 250

    def process_item(self, item, spider):
        self.batch.append(item)
        if len(self.batch) >= self.batch_size:
            d = deferToThread(self._process_batch)
            d.addErrback(lambda err: spider.logger.error(f"Batch error: {err}")) # Generic error message
        return item

    def _process_batch(self):
        texts = [itm['text'] for itm in self.batch]
        cleaned_texts = []
        if not self.use_cpu: # Use GPU processing if not in CPU mode
            processed_texts = self.gpu_processor.process_batch(texts)
            if processed_texts is None: # Handle potential GPU processing error
                cleaned_texts = texts # Fallback to original texts if GPU processing fails
                print("[TextPipeline] WARNING: GPU processing failed, falling back to CPU (no GPU cleaning).")
            else:
                cleaned_texts = processed_texts


            if self.target_language == 'gr' or self.target_language == 'greek': # Apply Greek filter if target language is Greek
                 final_cleaned_texts = []
                 for text in cleaned_texts:
                     # Apply GPU Greek filtering AGAIN after initial cleanup (ensure only greek chars remain after overall cleaning) - optional, could be redundant if GPU filter is robust enough
                     if not self.use_cpu and self.gpu_processor: # Use GPU filtering if GPU is enabled and processor available
                         gpu_cleaned_texts_secondary = self.gpu_processor.process_batch([text]) # Process each text individually on GPU for greek filtering
                         if gpu_cleaned_texts_secondary and gpu_cleaned_texts_secondary[0]: # Check if GPU processing was successful
                            final_cleaned_texts.append(gpu_cleaned_texts_secondary[0])
                         else: # Fallback to CPU-based normalization if secondary GPU filtering fails
                             normalized_text_cpu = ''.join(c for c in unicodedata.normalize('NFKC', text).strip() if self._is_greek_char(ord(c))) # CPU based greek char filter
                             final_cleaned_texts.append(normalized_text_cpu)
                     else: # CPU-based normalization and greek char filtering
                         normalized_text_cpu = ''.join(c for c in unicodedata.normalize('NFKC', text).strip() if self._is_greek_char(ord(c))) # CPU based greek char filter
                         final_cleaned_texts.append(normalized_text_cpu)
                 cleaned_texts = final_cleaned_texts # Update cleaned_texts with greek filtered texts
            else:
                print("[TextPipeline] No language specific filtering applied.") # Generic scraping, no language filtering

        else: # CPU mode - perform CPU based cleanup/normalization if needed. Now it only normalizes.
            print("[TextPipeline] Processing batch on CPU (GPU disabled). Applying basic unicode normalization.")
            cleaned_texts = [unicodedata.normalize('NFKC', text).strip() for text in texts] # Basic CPU normalization


        if not cleaned_texts:
            self.batch = [] # Clear batch if cleaning resulted in None or empty list
        else:
            for itm, text in zip(self.batch, cleaned_texts):
                itm['text'] = text
            self.batch = []

    def _is_greek_char(self, char_code):
        # CPU based greek character check - same ranges as GPU kernel
        c = char_code
        return (c >= 0x0370 and c <= 0x03FF) or \
            (c >= 0x1F00 and c <= 0x1FFF)  # Basic and Extended Greek Ranges (Emoji range removed for CPU check)

    def close_spider(self, spider):
        if self.batch:
            # Process any remaining items synchronously before closing.
            self._process_batch()


class StoragePipeline:
    def __init__(self, jobdir=None, output_file='scraped_data_robust.jsonl'): # Accept output_file - default is now generic filename
        print(f"[StoragePipeline] Initializing storage pipelines (JSON & JSONL), Output File: {output_file}...")
        self.output_file_name_jsonl = output_file # Use provided output_file name
        self.jsonl_file = open(self.output_file_name_jsonl, 'a', encoding='utf-8')
        self.json_data = []
        self.json_file_name = 'scraped_data_all_in_one.json' # Generic JSON filename
        if jobdir:
            print(f"[StoragePipeline] Resuming job from directory: {jobdir}")

    def process_item(self, item, spider):
        self.jsonl_file.write(json.dumps(item, ensure_ascii=False) + '\n')
        self.json_data.append(item)
        print(f"[StoragePipeline] Stored item from {item['url']}")
        return item

    def close_spider(self, spider):
        if self.jsonl_file:
            self.jsonl_file.close()
        if self.json_data:
            with open(self.json_file_name, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, ensure_ascii=False, indent=4)
            print(f"[StoragePipeline] JSON file saved: {self.json_file_name}")