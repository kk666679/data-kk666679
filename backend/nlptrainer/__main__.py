#!/usr/bin/env python3
"""
Fine-tune Bahasa Malaysia BERT model for HRMS
Usage: python -m nlptrainer --model=mesolitica/bert-base-bahasa --dataset=hrms_malaysian_reviews --epochs=3
"""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import json

class MalaysianHRMSTrainer:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=3  # positive, negative, neutral
        )
    
    def load_dataset(self, dataset_name: str) -> Dataset:
        """Load Malaysian HR dataset"""
        
        # Sample Malaysian HR feedback data
        data = [
            {"text": "Kerja di sini sangat mencabar tetapi bermanfaat", "label": 2},  # positive
            {"text": "Management tidak adil dalam pembahagian kerja", "label": 0},  # negative
            {"text": "Gaji berpatutan tapi beban kerja berat", "label": 1},  # neutral
            {"text": "Suasana kerja yang baik dan rakan sekerja yang membantu", "label": 2},
            {"text": "Tiada peluang kenaikan pangkat", "label": 0},
            {"text": "Faedah kesihatan yang baik", "label": 2},
            {"text": "Waktu kerja yang fleksibel", "label": 2},
            {"text": "Tekanan kerja yang tinggi", "label": 0},
        ]
        
        return Dataset.from_list(data)
    
    def tokenize_data(self, dataset: Dataset) -> Dataset:
        """Tokenize dataset for training"""
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding=True,
                max_length=512
            )
        
        return dataset.map(tokenize_function, batched=True)
    
    def train(self, dataset: Dataset, epochs: int = 3):
        """Fine-tune the model"""
        
        # Split dataset
        train_size = int(0.8 * len(dataset))
        train_dataset = dataset.select(range(train_size))
        eval_dataset = dataset.select(range(train_size, len(dataset)))
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir="./logs",
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Train model
        print(f"🚀 Starting fine-tuning of {self.model_name}")
        trainer.train()
        
        # Save model
        trainer.save_model("./fine_tuned_malaysian_hrms")
        self.tokenizer.save_pretrained("./fine_tuned_malaysian_hrms")
        
        print("✅ Fine-tuning completed!")
        return trainer

def main():
    parser = argparse.ArgumentParser(description="Fine-tune Bahasa Malaysia model for HRMS")
    parser.add_argument("--model", default="mesolitica/bert-base-bahasa", help="Base model to fine-tune")
    parser.add_argument("--dataset", default="hrms_malaysian_reviews", help="Dataset name")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    
    args = parser.parse_args()
    
    print(f"🇲🇾 Fine-tuning {args.model} for Malaysian HRMS")
    print(f"   Dataset: {args.dataset}")
    print(f"   Epochs: {args.epochs}")
    
    # Initialize trainer
    trainer = MalaysianHRMSTrainer(args.model)
    
    # Load and prepare dataset
    dataset = trainer.load_dataset(args.dataset)
    tokenized_dataset = trainer.tokenize_data(dataset)
    
    # Train model
    trainer.train(tokenized_dataset, args.epochs)

if __name__ == "__main__":
    main()