import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

class MalaysianHRModelTrainer:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, 
            num_labels=3  # positive, neutral, negative
        )

    def prepare_malaysian_dataset(self):
        """Prepare Malaysian HR-specific training data"""
        # Sample Malaysian HR feedback data
        data = [
            {"text": "Kerja sangat mencabar tapi bos memahami", "label": 1},  # positive
            {"text": "Work-life balance tidak seimbang", "label": 0},  # negative
            {"text": "Gaji okay tapi benefits boleh improve", "label": 2},  # neutral
            {"text": "Team spirit bagus, environment friendly", "label": 1},  # positive
            {"text": "Overtime selalu, penat sangat", "label": 0},  # negative
        ]
        
        df = pd.DataFrame(data)
        return Dataset.from_pandas(df)

    def tokenize_data(self, dataset):
        """Tokenize the dataset"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"], 
                truncation=True, 
                padding=True, 
                max_length=512
            )
        
        return dataset.map(tokenize_function, batched=True)

    def train_model(self):
        """Train the Malaysian HR sentiment model"""
        dataset = self.prepare_malaysian_dataset()
        tokenized_dataset = self.tokenize_data(dataset)
        
        training_args = TrainingArguments(
            output_dir="./malaysian_hr_model",
            num_train_epochs=3,
            per_device_train_batch_size=8,
            warmup_steps=100,
            logging_steps=10,
            save_strategy="epoch",
            evaluation_strategy="no",
            save_total_limit=2,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            tokenizer=self.tokenizer,
        )
        
        trainer.train()
        trainer.save_model("./malaysian_hr_model")
        
        return "Model training completed"

    def evaluate_model(self, test_texts):
        """Evaluate model on Malaysian HR texts"""
        inputs = self.tokenizer(test_texts, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        return predictions.numpy()

if __name__ == "__main__":
    trainer = MalaysianHRModelTrainer()
    result = trainer.train_model()
    print(f"✅ {result}")